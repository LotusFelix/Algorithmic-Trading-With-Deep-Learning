
import matplotlib.pyplot as plt

def plot_training_history(history, save_path: str):
    """Plots train vs val loss over epochs."""
    plt.figure()
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.title('Training History')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_predictions(y_true, y_pred, save_path: str, n_samples: int = 100):
    """Plots real vs predicted High/Low/Close on last n_samples."""
    if len(y_true) > n_samples:
        y_true = y_true[-n_samples:]
        y_pred = y_pred[-n_samples:]

    titles = ['High','Low','Close']
    fig, axes = plt.subplots(3, 1, figsize=(12,15))
    for i, title in enumerate(titles):
        axes[i].plot(y_true[:, i], label=f"Real {title}")
        axes[i].plot(y_pred[:, i], linestyle='--', label=f"Pred {title}")
        axes[i].set_title(title)
        axes[i].legend()
        axes[i].grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
