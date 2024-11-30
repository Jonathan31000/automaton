import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Exemple de données fictives
X_train = torch.rand((100, 10))
y_train = torch.randint(0, 2, (100,))
X_test = torch.rand((20, 10))
y_test = torch.randint(0, 2, (20,))

# Définir un modèle simple
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 2)
    
    def forward(self, x):
        return self.fc(x)

model = SimpleModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Entraînement
for epoch in range(20):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

# Évaluation
with torch.no_grad():
    y_pred = model(X_test).argmax(dim=1)
    accuracy = (y_pred == y_test).float().mean()
    print("Accuracy:", accuracy.item())
