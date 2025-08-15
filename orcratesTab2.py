import streamlit as st
import pandas as pd
from cratesData import *
def display():
    num_crates=st.session_state["num_crates"]
    crate_type=st.session_state["crate_type"]
    finish_chance=st.session_state["finish_chance"]
    rarity_probabilities=st.session_state["rarity_probabilities"]
    crates=st.session_state["crates"]
   
    # Update counters
    st.session_state['crates_opened'] += num_crates
    st.session_state['or_bucks_spent'] += num_crates * 800 # 800 = price for all crates currently
    st.session_state['crate_counts'][crate_type] += num_crates  # Update crate type counter

    # Initialize a list to store the results for the table
    results = []
    items_with_rarity = []

    # Open selected number of crates and collect results
    for i in range(num_crates):
        opened_items = crates[crate_type].open_crate(finish_chance,rarity_probabilities)
        results.append({
            "Item 1": str(opened_items[0]),  # Store just the display name
            "Item 2": str(opened_items[1]),
            "Item 3": str(opened_items[2])
        })

        # Collect items with their rarities for color coding
        items_with_rarity.extend(opened_items)

        # Update rarity and type counts
        for item in opened_items:
            if item.has_finish:
                st.session_state['rarity_counts']['Finish'] += 1
            st.session_state['rarity_counts'][item.rarity] += 1
            st.session_state['type_counts'][item.item_type] += 1

    # Convert results to a DataFrame for display
    results_df = pd.DataFrame(results)

    # Function to apply conditional formatting
    def highlight_cells(val):
        # Check if the item name contains any of the finish names
        for finish in finishes:
            if val.startswith(finish):  # Check if the value starts with a finish name
                return f'background-color: {finishes[finish]}; color: white;font-weight: bold;'
        
        # Match the display name with the corresponding item rarity
        for item in items_with_rarity:
            if item.display_name == val:
                rarity = item.rarity
                break
        else:
            rarity = None
        
        # Apply color based on the rarity of the item
        if rarity in rarity_color_map:
            color = rarity_color_map[rarity]
            return f'background-color: {color}; color: white'
        return ''

    # Calculate total money spent
    money_spent = st.session_state['or_bucks_spent'] * 0.005

    # Display the total crates opened, OR-Bucks spent, and money spent in USD, based on 0.005 per OR-Buck (biggest bundle price)
    st.subheader("Summary")
    st.success(f"Total Crates Opened: {st.session_state['crates_opened']}")
    st.success(f"Total OR-Bucks Spent: {st.session_state['or_bucks_spent']} (Total Money Spent: $USD {money_spent:.2f})")

    # Apply the style map function
    styled_df = results_df.style.map(highlight_cells)

    # Display the results table with formatting and no index
    st.subheader(f"Results for {crate_type} Crates:")
    st.dataframe(styled_df.hide(axis="index"))  # Hide the index

    # Statistics
    # Display statistics in the sidebar
    st.subheader("Statistics")
    
    rarity_counts = st.session_state['rarity_counts']
    type_counts = st.session_state['type_counts']
    crate_counts = st.session_state['crate_counts']

    # Create an expander for rarity counts
    with st.expander("Rarity Counts"):
        rarity_df = pd.DataFrame(rarity_counts.items(), columns=['Rarity', 'Count'])
        st.dataframe(rarity_df)

    # Create an expander for item type counts
    with st.expander("Item Type Counts"):
        type_df = pd.DataFrame(type_counts.items(), columns=['Item Type', 'Count'])
        st.dataframe(type_df)

    # Create an expander for crate type counts
    with st.expander("Crate Type Counts"):
        crate_df = pd.DataFrame(crate_counts.items(), columns=['Crate Type', 'Count'])

        st.dataframe(crate_df)


