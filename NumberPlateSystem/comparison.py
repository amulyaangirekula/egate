# import matplotlib.pyplot as plt
# import numpy as np

# # Metrics for comparison
# metrics = ['Accuracy (%)', 'Training Time (Minutes)', 'Processing Time', 'Development Effort (0-10)', 'Resources Needed (0-10)', 'Flexibility (0-10)', 'Scalability (0-10)']
# opencv_cnn = [85, 48, 2.3, 8, 9, 9, 6]
# gemini_api = [95, 0, 0.5, 3, 2, 7, 9]

# x = np.arange(len(metrics))
# width = 0.35

# fig, ax = plt.subplots(figsize=(10,6))

# # Bars for OpenCV+CNN and Gemini API
# rects1 = ax.bar(x - width/2, opencv_cnn, width, label='OpenCV+CNN')
# rects2 = ax.bar(x + width/2, gemini_api, width, label='Gemini API')

# ax.set_ylabel('Scores')
# ax.set_title('Comparison of OpenCV+CNN and Gemini API')
# ax.set_xticks(x)
# ax.set_xticklabels(metrics, rotation=30, ha='right')
# ax.legend()
# ax.grid(axis='y')

# plt.tight_layout()
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def create_simple_comparison_graph(save_path='model_comparison.png'):
    # Set the style
    plt.style.use('ggplot')
    sns.set_palette("Set2")
    
    # Create a figure
    plt.figure(figsize=(12, 8))
    
    # Define metrics and models
    metrics = ['Processing Speed (FPS)', 'Memory Usage (MB)', 'Setup Time (min)', 'Accuracy (%)']
    
    # Sample data - replace with your actual measurements
    opencv_values = [25, 45, 15, 92]  # OpenCV HaarCascade
    yolo_values = [15, 250, 60, 96]   # YOLO
    
    # Set positions and width for bars
    x = np.arange(len(metrics))
    width = 0.35
    
    # Create bars
    plt.bar(x - width/2, opencv_values, width, label='OpenCV HaarCascade', color='#3498db')
    plt.bar(x + width/2, yolo_values, width, label='YOLO', color='#e74c3c')
    
    # Add labels, title and legend
    plt.xlabel('Performance Metrics', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.title('OpenCV HaarCascade vs YOLO Comparison', fontsize=16, fontweight='bold')
    plt.xticks(x, metrics, fontsize=12)
    plt.legend(fontsize=12)
    
    # Add value labels on top of each bar
    for i, v in enumerate(opencv_values):
        plt.text(i - width/2, v + 2, str(v), ha='center', fontweight='bold')
        
    for i, v in enumerate(yolo_values):
        plt.text(i + width/2, v + 2, str(v), ha='center', fontweight='bold')
    
    # Add a note about the chart
    plt.figtext(0.5, 0.01, 
                "Note: Higher values for Processing Speed and Accuracy are better.\nLower values for Memory Usage and Setup Time are better.", 
                ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
    
    # Ensure layout is tight
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the figure
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    return f"Comparison graph saved to {save_path}"

# Generate radar chart for visual comparison of overall capability
def create_radar_chart(save_path='model_radar_comparison.png'):
    # Create figure
    plt.figure(figsize=(10, 8))
    
    # Categories for comparison
    categories = ['Speed', 'Resource Efficiency', 'Ease of Setup', 
                  'Portability', 'Cost Effectiveness']
    
    # Values for each category (scale of 0-5, 5 being best)
    opencv_values = [4.5, 4.8, 5.0, 4.7, 4.9]
    yolo_values = [3.0, 2.0, 2.5, 2.8, 2.2]
    
    # Create angles for each category
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    
    # Close the polygon
    angles += angles[:1]
    opencv_values += opencv_values[:1]
    yolo_values += yolo_values[:1]
    categories += categories[:1]
    
    # Create the plot
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, opencv_values, 'o-', linewidth=2, label='OpenCV HaarCascade')
    ax.plot(angles, yolo_values, 's-', linewidth=2, label='YOLO')
    ax.fill(angles, opencv_values, alpha=0.25)
    ax.fill(angles, yolo_values, alpha=0.25)
    
    # Set category labels
    ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
    
    # Set radial limits
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    
    # Add labels
    plt.title('OpenCV HaarCascade vs YOLO: Feature Comparison', fontsize=16, fontweight='bold')
    plt.legend(loc='upper right', fontsize=12)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    return f"Radar comparison chart saved to {save_path}"

if __name__ == "__main__":
    create_simple_comparison_graph()
    create_radar_chart()
    print("Comparison graphs created successfully!")