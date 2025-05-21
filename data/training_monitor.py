import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(128, 64)  # 第一层全连接层
        self.fc2 = nn.Linear(64, 32)   # 第二层全连接层
        self.fc3 = nn.Linear(32, 2)    # 第三层全连接层

    def forward(self, x):
        out = torch.relu(self.fc1(x))   # 第一层+ReLU激活
        out = torch.relu(self.fc2(out)) # 第二层+ReLU激活
        out = self.fc3(out)             # 第三层输出
        return out

# 生成模拟数据，1000个样本，每个样本128维
data = torch.randn(1000, 128)  # 示例数据
labels = torch.randint(0, 2, (1000,))  # 示例二分类标签
dataset = TensorDataset(data, labels)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)  # 构建数据加载器

# 初始化模型和优化器
model = SimpleModel()
criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器

# TensorBoard初始化
writer = SummaryWriter(log_dir='logs')

# 训练模型
def train_model(model, train_loader, criterion, optimizer, writer, num_epochs = 100):
    for epoch in range(num_epochs):
        epoch_loss = 0
        correct = 0
        total = 0

        for batch_data, batch_labels in train_loader:
            optimizer.zero_grad()  # 梯度清零
            # 前向传播
            outputs = model(batch_data)
            loss = criterion(outputs, batch_labels)

            # 反向传播和优化
            loss.backward()
            optimizer.step()

            # 更新损失
            epoch_loss += loss.item()

            # 计算准确率
            _, predicted = torch.max(outputs.data, 1)
            total += batch_labels.size(0)
            correct += (predicted == batch_labels).sum().item()

        # 记录每个epoch的损失值到TensorBoard
        epoch_loss /= len(train_loader)
        accuracy = 100 * correct / total
        writer.add_scalar('Loss/train', epoch_loss, epoch)
        writer.add_scalar('Accuracy/train', accuracy, epoch)
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss/len(train_loader):.4f}')

# 开始训练
train_model(model, train_loader, criterion, optimizer, writer)
# 关闭TensorBoard
writer.close()