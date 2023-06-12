import matplotlib.pyplot as plt

def plot_fit_result(train_loss_list,train_acc_list, val_loss_list, val_acc_list):
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.title('Loss')
    plt.plot(train_loss_list,label='Train')
    plt.plot(val_loss_list,label='Validation')
    plt.legend()

    plt.subplot(1,2,2)
    plt.title('Accuracy')
    plt.plot(train_acc_list,label='Train')
    plt.plot(val_acc_list,label='Validation')
    plt.legend()

    plt.tight_layout()
    plt.show()
