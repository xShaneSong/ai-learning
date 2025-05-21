import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class SimpleModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_rate):
        super(SimpleModel, self).__init__()
        # 第一层全连接层
        self.fc1 = nn.Linear(input_size, hidden_size)
        # Dropout层，防止过拟合
        self.dropout = nn.Dropout(dropout_rate)
        # self.relu = nn.ReLU()  # 也可以用ReLU激活函数
        # 第二层全连接层
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # 第一层+ReLU激活
        out = torch.relu(self.fc1(x))
        # out = self.fc1(x)
        # out = self.relu(out)
        # Dropout
        out = self.dropout(out)
        # 输出层
        out = self.fc2(out)
        return out

# 生成模拟数据，1000个样本，每个样本128维
data = torch.randn(1000, 128)  # 示例数据
labels = torch.randint(0, 2, (1000,))  # 示例二分类标签
dataset = TensorDataset(data, labels)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)  # 构建数据加载器

# 超参数设置
input_size = 128      # 输入特征维度
hidden_size = 64      # 隐藏层神经元数
output_size = 2       # 输出类别数
dropout_rate = 0.5    # Dropout比例
learning_rate = 0.001 # 学习率
num_epochs = 10       # 训练轮数

model = SimpleModel(input_size, hidden_size, output_size, dropout_rate)
criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
optimizer = optim.Adam(model.parameters(), lr=learning_rate)  # Adam优化器

def train_model(model, train_loader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        epoch_loss = 0
        for batch_data, batch_labels in train_loader:
            optimizer.zero_grad()  # 梯度清零
            # 前向传播
            outputs = model(batch_data)
            loss = criterion(outputs, batch_labels)

            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss/len(train_loader):.4f}")

train_model(model, train_loader, criterion, optimizer, num_epochs)

#- 根据需要调整 `n_trials`（搜索次数）、`num_epochs`（每次训练轮数）等参数。
#- 这里用最后一个batch的loss作为目标值，实际项目中建议用验证集准确率或loss。
def objective(trial):
    # 定义要优化的超参数空间
    hidden_size = trial.suggest_int('hidden_size', 32, 128)
    dropout_rate = trial.suggest_float('dropout_rate', 0.1, 0.7)
    learning_rate = trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True)
    num_epochs = 20  # 为了加速搜索，这里用较少的epoch

    model = SimpleModel(input_size, hidden_size, output_size, dropout_rate)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # 简单训练循环
    for epoch in range(num_epochs):
        for batch_data, batch_labels in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_data)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()

    # 简单评估：用最后一个batch的loss作为目标
    return loss.item()

# 使用Optuna进行超参数搜索
import optuna
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=50)

print("最优超参数：", study.best_params)
print("最优loss：", study.best_value)

# # 以下为sklearn的网格搜索超参数示例
# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestClassifier

# param_grid = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5, 10],
#     # 'min_samples_leaf': [1, 2, 4],
# #    'max_features': ['auto', 'sqrt', 'log2']
# }

# rf = RandomForestClassifier()

# grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, verbose=2, scoring='accuracy')
# grid_search.fit(data.numpy(), labels.numpy())

# print("Best parameters found: ", grid_search.best_params_)
# print("Best cross-validation score: ", grid_search.best_score_)