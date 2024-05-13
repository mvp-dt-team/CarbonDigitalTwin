import torch.nn as nn


class NNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, hidden_size_two, hidden_size_three, output_size):
        super(NNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size_two, bias=True)
        self.relu = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size_two, hidden_size_three, bias=True)
        self.fc4 = nn.Linear(hidden_size_three, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        return x
