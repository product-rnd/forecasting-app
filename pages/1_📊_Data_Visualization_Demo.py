import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Function to wrangle data
def wrangle_data(file_path):
    sales = pd.read_csv(file_path)
    # Convert date columns to datetime format
    date_cols = ['Order Date', 'Ship Date']
    for col in date_cols:
        sales[col] = pd.to_datetime(sales[col], format='%m/%d/%Y')
    # Add new columns
    sales['Order Year'] = sales['Order Date'].dt.to_period('Y')
    sales['Order Month'] = sales['Order Date'].dt.month_name()
    sales['Order Day'] = sales['Order Date'].dt.day_name()
    sales['Date_diff'] = sales['Ship Date'] - sales['Order Date']
    return sales

# Load data
file_path = 'data_input/wahmart_data.csv'
sales = wrangle_data(file_path)

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Set style for plots
plt.style.use('seaborn-v0_8-whitegrid') 
color = sns.palettes.mpl_palette('Paired')

# Function to plot daily sales
def plot_daily_data(data, column_name):
    data_grouped = data.groupby('Order Day').agg({
        'Order ID': 'count',
        column_name: 'sum'
    }).reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    data_grouped.plot(x="Order Day", y=column_name, ax=ax, color=color[2])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xlabel('Order Day')
    plt.ylabel(f'Total {column_name.capitalize()}')
    plt.title(f'Daily {column_name.capitalize()} Wahmart.inc 2020-2023')
    plt.legend(title='Category')
    st.pyplot(fig)

# Function to plot monthly data
def plot_monthly_data(data, column_name):
    data_grouped = data.sort_values(by='Order Month').groupby(['Order Month', 'Order Year']).agg({
        'Order ID': 'count',
        column_name: 'sum'
    }).reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    data_grouped.pivot(index='Order Month', columns='Order Year', values=column_name).plot(ax=ax, color=color)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xlabel('Month')
    plt.ylabel(f'Total {column_name.capitalize()} in $')
    plt.title(f'Monthly {column_name.capitalize()} Wahmart.inc 2020-2023')
    plt.xticks(range(len(months)), months)
    st.pyplot(fig)

# Function to plot category-wise data
def plot_category_data(data, column_name):
    category_sales = data.groupby('Category')[column_name].sum().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    category_sales.plot(kind='barh', color=color)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xlabel(f'Total {column_name} ($)')
    plt.ylabel('Category')
    plt.title(f'Total {column_name} by Category')
    st.pyplot(fig)

# Function to plot monthly sales by category
def plot_monthly_sales_by_category(sales, column_name):
    monthsales = sales.groupby(['Order Month', 'Category'])[column_name].sum().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    monthsales.plot(kind='bar', color=color, ax=ax)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xlabel('Order Month')
    plt.ylabel(f'Total {column_name}')
    plt.title(f'Monthly {column_name} by Category (Stacked)')
    plt.legend(title='Category')
    plt.xticks(range(len(months)), months, rotation=45)
    st.pyplot(fig)


# Streamlit app
def main():
    st.set_page_config(page_title='Walmart Inc. Sales and Profit Visualization', layout='wide')

    # Create input to choose between sales and profit
    data_type = st.sidebar.selectbox("Select data type:", ["Sales", "Profit"])

    st.title(f'Walmart Inc. {data_type} Visualization')

    st.markdown(
        """
        🗃️ The dataset we use comes from a retail company called Walmart Inc. 
        The company already operates in the United States and Canada. 
        Walmart provides various types of products from electronics, office supplies, to household appliances. Wahmart is committed to always providing the best quality products and always prioritizing customer satisfaction.
        """
    )

    st.write(sales.head())

    # Create columns for layout
    # col1, col2 = st.columns(2)

    # Daily data Trend
    st.header('Daily {} Trend'.format(data_type))
    plot_daily_data(sales, data_type)

    # Monthly data Trend
    st.header('Monthly {} Trend'.format(data_type))
    plot_monthly_data(sales, data_type)

    # Category-wise data
    st.header('Category-wise {} Trend'.format(data_type))
    plot_category_data(sales, data_type)

    # Monthly data by Category
    st.header('Monthly {} by Category'.format(data_type))
    plot_monthly_sales_by_category(sales, data_type)

    # Copyright notice
    st.sidebar.write('---')
    st.sidebar.write("© Product Team Algoritma, 2024")

if __name__ == '__main__':
    main()
