from typing import List
import cv2
import numpy as np
from typing import Tuple
from collections import namedtuple
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
Batch = namedtuple('Batch', 'imgs, gt_texts, batch_size')
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
class Preprocessor:
    def __init__(self,
                 img_size: Tuple[int, int],
                 padding: int = 0) -> None:

        self.img_size = img_size
        self.padding = padding

    def process_img(self, img: np.ndarray) -> np.ndarray:
        if img is None:
            img = np.zeros(self.img_size[::-1])
        img = img.astype(float)
        ht = self.img_size[1]
        h, w = img.shape
        f = ht / h
        wt = int(f * w + self.padding)
        wt = wt + (4 - wt) % 4
        tx = (wt - w * f) / 2
        ty = 0

        # map image into target image
        M = np.float32([[f, 0, tx], [0, f, ty]])
        target = np.ones([ht, wt]) * 255
        img = cv2.warpAffine(img, M, dsize=(wt, ht), dst=target, borderMode=cv2.BORDER_TRANSPARENT)

        # transpose for TF
        img = cv2.transpose(img)

        # convert to range [-1, 1]
        img = img / 255 - 0.5
        return img

tf.compat.v1.disable_eager_execution()

class Model:
    def __init__(self,
                 char_list: List[str],
                 decoder_type: str = 0,
                 must_restore: bool = True) -> None:
        """Init model: add CNN, RNN and CTC and initialize TF."""
        self.char_list = char_list
        self.decoder_type = decoder_type
        self.must_restore = must_restore

        # input image batch
        self.input_imgs = tf.compat.v1.placeholder(tf.float32, shape=(None, None, None))

        # setup CNN, RNN and CTC
        self.setup_cnn()
        self.setup_rnn()
        self.setup_ctc()

        # initialize TF
        self.sess = self.setup_tf()

    def setup_cnn(self) -> None:
        """Create CNN layers."""
        cnn_in4d = tf.expand_dims(input=self.input_imgs, axis=3)
        kernel_vals = [5, 5, 3, 3, 3]
        feature_vals = [1, 32, 64, 128, 128, 256]
        stride_vals = pool_vals = [(2, 2), (2, 2), (1, 2), (1, 2), (1, 2)]
        num_layers = len(stride_vals)
        pool = cnn_in4d  # input to first CNN layer
        for i in range(num_layers):
            kernel = tf.Variable(
                tf.random.truncated_normal([kernel_vals[i], kernel_vals[i], feature_vals[i], feature_vals[i + 1]],
                                           stddev=0.1))
            conv = tf.nn.conv2d(input=pool, filters=kernel, padding='SAME', strides=(1, 1, 1, 1))
            conv_norm = tf.compat.v1.layers.batch_normalization(conv)
            relu = tf.nn.relu(conv_norm)
            pool = tf.nn.max_pool2d(input=relu, ksize=(1, pool_vals[i][0], pool_vals[i][1], 1),
                                    strides=(1, stride_vals[i][0], stride_vals[i][1], 1), padding='VALID')

        self.cnn_out_4d = pool

    def setup_rnn(self) -> None:
        rnn_in3d = tf.squeeze(self.cnn_out_4d, axis=[2])
        num_hidden = 256
        cells = [tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=num_hidden, state_is_tuple=True) for _ in
                 range(2)]  # 2 layers
        stacked = tf.compat.v1.nn.rnn_cell.MultiRNNCell(cells, state_is_tuple=True)
        (fw, bw), _ = tf.compat.v1.nn.bidirectional_dynamic_rnn(cell_fw=stacked, cell_bw=stacked, inputs=rnn_in3d,
                                                                dtype=rnn_in3d.dtype)
        concat = tf.expand_dims(tf.concat([fw, bw], 2), 2)
        kernel = tf.Variable(tf.random.truncated_normal([1, 1, num_hidden * 2, len(self.char_list) + 1], stddev=0.1))
        self.rnn_out_3d = tf.squeeze(tf.nn.atrous_conv2d(value=concat, filters=kernel, rate=1, padding='SAME'),
                                     axis=[2])

    def setup_ctc(self) -> None:
        self.ctc_in_3d_tbc = tf.transpose(a=self.rnn_out_3d, perm=[1, 0, 2])
        self.gt_texts = tf.SparseTensor(tf.compat.v1.placeholder(tf.int64, shape=[None, 2]),
                                        tf.compat.v1.placeholder(tf.int32, [None]),
                                        tf.compat.v1.placeholder(tf.int64, [2]))
        self.seq_len = tf.compat.v1.placeholder(tf.int32, [None])
        self.loss = tf.reduce_mean(
            input_tensor=tf.compat.v1.nn.ctc_loss(labels=self.gt_texts, inputs=self.ctc_in_3d_tbc,
                                                  sequence_length=self.seq_len,
                                                  ctc_merge_repeated=True))
        self.saved_ctc_input = tf.compat.v1.placeholder(tf.float32,
                                                        shape=[None, None, len(self.char_list) + 1])
        self.loss_per_element = tf.compat.v1.nn.ctc_loss(labels=self.gt_texts, inputs=self.saved_ctc_input,
                                                         sequence_length=self.seq_len, ctc_merge_repeated=True)
        self.decoder = tf.nn.ctc_greedy_decoder(inputs=self.ctc_in_3d_tbc, sequence_length=self.seq_len)

    def setup_tf(self) -> Tuple[tf.compat.v1.Session, tf.compat.v1.train.Saver]:
        sess = tf.compat.v1.Session()
        model_dir = 'model/'
        latest_snapshot = tf.train.latest_checkpoint(model_dir)  # is there a saved model?
        tf.compat.v1.train.Saver(max_to_keep=1).restore(sess, latest_snapshot)
        return sess

    def decoder_output_to_text(self, ctc_output: tuple, batch_size: int) -> List[str]:
        decoded = ctc_output[0][0]

        label_strs = [[] for _ in range(batch_size)]

        for (idx, idx2d) in enumerate(decoded.indices):
            label = decoded.values[idx]
            batch_element = idx2d[0]  # index according to [b,t]
            label_strs[batch_element].append(label)

        # map labels to chars for all batch elements
        return [''.join([self.char_list[c] for c in labelStr]) for labelStr in label_strs]


    def infer_batch(self, batch: Batch):
        """Feed a batch into the NN to recognize the texts."""
        # decode, optionally save RNN output
        num_batch_elements = len(batch.imgs)
        # put tensors to be evaluated into list
        eval_list = []
        eval_list.append(self.decoder)
        # sequence length depends on input image size (model downsizes width by 4)
        max_text_len = batch.imgs[0].shape[0] // 4
        # dict containing all tensor fed into the model
        feed_dict = {self.input_imgs: batch.imgs, self.seq_len: [max_text_len] * num_batch_elements}
        # evaluate model
        eval_res = self.sess.run(eval_list, feed_dict)
        decoded = eval_res[0]
        # map labels (numbers) to character string
        texts = self.decoder_output_to_text(decoded, num_batch_elements)

        return texts


def infer(model: Model, fn_img: List[str]) -> None:
    """Recognizes text in image provided by file path."""
    lst_img = []
    for i in fn_img:
        img = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
        assert img is not None

        preprocessor = Preprocessor((128, 32), padding=16)
        img = preprocessor.process_img(img)
        lst_img.append(img)
    lst_result = []
    for i in lst_img:
        batch = Batch([i], None, 1)
        recognized = model.infer_batch(batch)
        lst_result.append(recognized[0])
    return lst_result
