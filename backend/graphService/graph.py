from config import MAX_GRAPH_NUMRIC , MAX_GRAPH_CATEGORY
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import base64
import io
    

def create_bar_chart(df, x_col, y_col):
    try:
        print(f"----------Make bar chart {x_col} : {y_col}")
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8, 6))
        sns.barplot(x=x_col, y=y_col, data=df)
        plt.title(f'{x_col} VS {y_col}')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return plot_base64

    except Exception as e:
        print(f"Error - graph: {e}")
        return None
    
def create_line_chart(df, x_col, y_col):
    try:
        print(f"----------make line chart of {x_col} : {y_col}")
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8, 6))
        sns.lineplot(x=x_col, y=y_col, data=df)
        plt.title(f'{x_col} VS {y_col}')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return plot_base64
    except Exception as e:
        print(f"Error - graph: {e}")
        return None

def create_scatter_plot(df, x_col, y_col):
    try:
        print(f"----------Make scatter plot of {x_col} : {y_col}")
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=x_col, y=y_col, data=df)
        plt.title(f'{x_col} VS {y_col}')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return plot_base64
    except Exception as e:
        print(f"Error - graph: {e}")
        return None

def create_pie_chart_from_category(df, category_col):
    try:
        # Count the frequency of each category
        print(f"-------------Make pie of {category_col}-----------")
        category_counts = df[category_col].value_counts()
        
        # Create a pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title(f'Chart of {category_col}')
    
        # Save the plot to a binary buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return plot_base64
    except Exception as e:
        print(f"Error - graph: {e}")
        return None
    
def create_barplot_category(df, category_col):
    try:
        # Count the frequency of each category
        print(f"-------------Make barplot of {category_col}-----------")
        category_counts = df[category_col].value_counts()

        # Create the bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x=category_counts.index, y=category_counts.values, hue=category_counts.index, legend=False)
        plt.xlabel(category_col)
        plt.ylabel('Count')
        plt.title(f'Bar of {category_col}')
    
        # Save the plot to a binary buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return plot_base64
    except Exception as e:
        print(f"Error - graph: {e}")
        return None


def MakeGraphNumric(dfGraph: pd.DataFrame , interstingCol:str , top_Correlation: list[str]):
    try:
        graphNumric = []
        for i in range(min(MAX_GRAPH_NUMRIC ,len(top_Correlation))):
            random_int = random.randint(1, MAX_GRAPH_NUMRIC)
            if random_int == 1:
                graphNumric.append(create_bar_chart(dfGraph , interstingCol , top_Correlation.index[i]))
            elif random_int == 2:
                graphNumric.append(create_scatter_plot(dfGraph , interstingCol , top_Correlation.index[i]))
            else:
                graphNumric.append(create_line_chart(dfGraph , interstingCol , top_Correlation.index[i]))

        return graphNumric
    except Exception as e:
        return ""
    
    
def MakeGraphCategory(dfGraph: pd.DataFrame , columns: list[str]):
    try:
        graphCategory = []
        for i in range(min(MAX_GRAPH_CATEGORY ,len(columns))):
            random_int = random.randint(1, MAX_GRAPH_CATEGORY)
            if random_int == 1:
                graphCategory.append(create_pie_chart_from_category(dfGraph , columns[i]))
            else:
                graphCategory.append(create_barplot_category(dfGraph , columns[i]))

        return graphCategory
    except Exception as e:
        return ""