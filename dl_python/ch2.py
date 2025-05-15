import keras
from keras.datasets import mnist

# 加载MNIST数据集
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print(train_images.shape)  # 输出训练图像的形状
print(len(train_labels))   # 输出训练标签的数量
print(train_labels)        # 输出训练标签
print(test_images.shape)   # 输出测试图像的形状
print(len(test_labels))    # 输出测试标签的数量

# digit = train_images[4]  # 选择第5张图像
# import matplotlib.pyplot as plt
# plt.imshow(digit, cmap=plt.cm.binary)  # 显示图像
# plt.show()

from keras import models
from keras import layers

# 定义神经网络模型
# network = models.Sequential()
# network.add(layers.Dense(512, activation='relu', input_shape=(28*28,)))
# network.add(layers.Dense(10, activation='softmax'))

# 使用另一种方式定义神经网络模型
network = models.Sequential([
    keras.Input(shape=(28*28,)),  # 输入层，输入形状为28*28
    layers.Dense(512, activation='relu'),  # 隐藏层，512个神经元，激活函数为ReLU
    layers.Dense(10, activation='softmax')  # 输出层，10个神经元，激活函数为softmax
])
print(network.summary())  # 打印模型摘要信息
network.compile(optimizer='rmsprop',  # 编译模型，优化器为rmsprop
                loss='categorical_crossentropy',  # 损失函数为categorical_crossentropy
                metrics=['accuracy'])  # 评估指标为准确率

# 预处理训练图像数据
train_images = train_images.reshape((60000, 28*28))  # 将训练图像数据重塑为60000行，每行28*28个像素
train_images = train_images.astype('float32') / 255  # 将像素值归一化到0-1之间

# 预处理测试图像数据
test_images = test_images.reshape((10000, 28*28))  # 将测试图像数据重塑为10000行，每行28*28个像素
test_images = test_images.astype('float32') / 255  # 将像素值归一化到0-1之间

from keras.utils import to_categorical

# 将训练标签进行one-hot编码
train_labels = to_categorical(train_labels)
# 将测试标签进行one-hot编码
test_labels = to_categorical(test_labels)
# 训练模型，训练数据为train_images和train_labels，训练5个周期，每批次128个样本
network.fit(train_images, train_labels, epochs=5, batch_size=128)

# 评估模型在测试数据上的表现
test_loss, test_acc = network.evaluate(test_images, test_labels)
print('test_acc:', test_acc)  # 输出测试准确率