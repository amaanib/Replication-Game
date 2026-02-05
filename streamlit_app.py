import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

# Replication Dynamics Game - Latest Version
st.set_page_config(page_title="Replication Dynamics Game", layout="wide")
st.title("🎮 Replication Dynamics Game")

# Define the automatons
automatons = ["DOVE", "HAWK", "GRIM", "TIT-FOR-TAT", "TAT-FOR-TIT", 
              "TWEEDLEDUM", "TWEEDLEDEE", "TWEETYPIE"]

# Default Payoff matrix
default_payoff_matrix = {
    "DOVE":        {"DOVE": 1,    "HAWK": -0.5, "GRIM": 1,    "TIT-FOR-TAT": 1,    "TAT-FOR-TIT": 1,    "TWEEDLEDUM": 1,    "TWEEDLEDEE": 1,    "TWEETYPIE": -0.5},
    "HAWK":        {"DOVE": 3,    "HAWK": 0,    "GRIM": 0,    "TIT-FOR-TAT": 0,    "TAT-FOR-TIT": 1.5,  "TWEEDLEDUM": 1.5,  "TWEEDLEDEE": 1.5,  "TWEETYPIE": 3},
    "GRIM":        {"DOVE": 2,    "HAWK": 0,    "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 0,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": -1},
    "TIT-FOR-TAT": {"DOVE": 2,    "HAWK": 0,    "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2/3,  "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TAT-FOR-TIT": {"DOVE": -0.5, "HAWK": 0.75, "GRIM": 0,    "TIT-FOR-TAT": 2/3,  "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TWEEDLEDUM":  {"DOVE": 2,    "HAWK": 0.75, "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TWEEDLEDEE":  {"DOVE": 2,    "HAWK": 0.75, "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TWEETYPIE":   {"DOVE": -0.5, "HAWK": 3,    "GRIM": -1,   "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
}

def simulate_replication_dynamics(num_periods=100, payoff_matrix=None):
    if payoff_matrix is None:
        payoff_matrix = default_payoff_matrix
    
    n_automatons = len(automatons)
    probabilities = np.ones(n_automatons) / n_automatons
    history = [probabilities.copy()]
    payoff_history = defaultdict(list)
    strategy_history = []
    payoff_matrices = []
    pairwise_payoffs_history = []  # Track pairwise payoffs for each round
    
    for period in range(num_periods):
        payoffs = np.zeros(n_automatons)
        
        # Store pairwise payoffs for this period
        pairwise_payoffs_period = pd.DataFrame(
            0.0,
            index=automatons,
            columns=automatons
        )
        
        for i, automaton_i in enumerate(automatons):
            for j, automaton_j in enumerate(automatons):
                pairwise_payoff = payoff_matrix[automaton_i][automaton_j] * probabilities[j]
                pairwise_payoffs_period.loc[automaton_i, automaton_j] = pairwise_payoff
                payoffs[i] += pairwise_payoff
        
        pairwise_payoffs_history.append(pairwise_payoffs_period)
        
        # Store current payoff matrix with period starting from t=0
        payoff_matrix_period = pd.DataFrame(
            payoffs.reshape(-1, 1),
            index=automatons,
            columns=[f"t={period}"]
        )
        payoff_matrices.append(payoff_matrix_period)
        
        # Determine dominant strategy for each automaton
        period_strategies = {}
        for i, automaton in enumerate(automatons):
            best_opponent_idx = np.argmax([payoff_matrix[automaton][opp] for opp in automatons])
            period_strategies[automaton] = automatons[best_opponent_idx]
        
        strategy_history.append(period_strategies)
        
        for i, automaton in enumerate(automatons):
            payoff_history[automaton].append(payoffs[i])
        
        min_payoff = np.min(payoffs)
        if min_payoff < 0:
            payoffs_adjusted = payoffs - min_payoff + 1
        else:
            payoffs_adjusted = payoffs + 1
        
        probabilities = probabilities * payoffs_adjusted
        probabilities = probabilities / np.sum(probabilities)
        history.append(probabilities.copy())
    
    return np.array(history), payoff_history, strategy_history, payoff_matrices, pairwise_payoffs_history

# Sidebar
with st.sidebar:
    st.header("Settings")
    num_periods = st.slider("Simulation Periods", 10, 200, 100)
    
    st.markdown("---")
    st.header("Payoff Matrix")
    
    # Option to edit payoff matrix
    use_custom_payoff = st.checkbox("Edit Payoff Matrix", value=False)
    
    if use_custom_payoff:
        st.markdown("### Customize Payoffs")
        st.write("Edit payoffs for each automaton vs opponent:")
        
        # Create editable payoff matrix
        custom_payoff_data = {}
        for automaton in automatons:
            st.markdown(f"**{automaton}:**")
            row_data = {}
            cols = st.columns(4)
            for idx, opponent in enumerate(automatons):
                col = cols[idx % 4]
                default_val = default_payoff_matrix[automaton][opponent]
                row_data[opponent] = col.number_input(
                    f"{automaton} vs {opponent}",
                    value=float(default_val),
                    step=0.1,
                    label_visibility="collapsed"
                )
            custom_payoff_data[automaton] = row_data
        
        payoff_matrix = custom_payoff_data
    else:
        payoff_matrix = default_payoff_matrix
        st.markdown("### Using Default Payoff Matrix")
        # Display default matrix
        default_df = pd.DataFrame(default_payoff_matrix).T
        st.dataframe(default_df, use_container_width=True)

st.info("📊 8 Automatons | ⏱️ Starting: 1/8 each | 🔄 Payoff-based reweighting")

if st.button("🎮 Run Simulation", use_container_width=True):
    with st.spinner("Running simulation..."):
        history, payoff_history, strategy_history, payoff_matrices, pairwise_payoffs_history = simulate_replication_dynamics(
            num_periods, 
            payoff_matrix
        )
    
    st.session_state.history = history
    st.session_state.payoff_history = payoff_history
    st.session_state.strategy_history = strategy_history
    st.session_state.payoff_matrices = payoff_matrices
    st.session_state.pairwise_payoffs_history = pairwise_payoffs_history
    st.session_state.done = True

if "done" in st.session_state and st.session_state.done:
    history = st.session_state.history
    payoff_history = st.session_state.payoff_history
    strategy_history = st.session_state.strategy_history
    payoff_matrices = st.session_state.payoff_matrices
    pairwise_payoffs_history = st.session_state.pairwise_payoffs_history
    final_probs = history[-1]
    
    st.header("Results")
    
    final_df = pd.DataFrame({
        "Automaton": automatons,
        "Probability": final_probs,
        "Percentage": final_probs * 100
    }).sort_values("Probability", ascending=False)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Top", final_df.iloc[0]["Automaton"], f"{final_df.iloc[0]['Percentage']:.1f}%")
    col2.metric("📉 Bottom", final_df.iloc[-1]["Automaton"], f"{final_df.iloc[-1]['Percentage']:.1f}%")
    col3.metric("Concentration", f"{np.sum(final_probs**2):.3f}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(final_df, values="Probability", names="Automaton", title="Final Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.dataframe(final_df[["Automaton", "Percentage"]], use_container_width=True)
    
    st.divider()
    st.subheader("Evolution Over Time")
    
    evolution_df = pd.DataFrame(history, columns=automatons)
    evolution_df['t'] = range(len(history))
    
    fig_evolution = go.Figure()
    for automaton in automatons:
        fig_evolution.add_trace(go.Scatter(
            x=evolution_df['t'],
            y=evolution_df[automaton],
            mode='lines',
            name=automaton,
            stackgroup='one'
        ))
    
    fig_evolution.update_layout(
        title="Probability Evolution (Stacked)",
        xaxis_title="Time Period (t)",
        yaxis_title="Probability",
        height=400
    )
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    st.subheader("Payoffs Over Time")
    payoff_df = pd.DataFrame(payoff_history)
    payoff_df['t'] = range(len(payoff_df))
    
    fig_payoff = go.Figure()
    for automaton in automatons:
        fig_payoff.add_trace(go.Scatter(
            x=payoff_df['t'],
            y=payoff_df[automaton],
            mode='lines',
            name=automaton
        ))
    
    fig_payoff.update_layout(
        title="Average Payoffs",
        xaxis_title="Time Period (t)",
        yaxis_title="Payoff",
        height=400
    )
    st.plotly_chart(fig_payoff, use_container_width=True)
    
    st.divider()
    st.subheader("📊 Detailed Period Analysis")
    
    # Allow user to select which periods to view
    periods_to_view = st.slider("Select periods to display", 0, len(payoff_history[automatons[0]]) - 1, (0, min(10, len(payoff_history[automatons[0]]) - 1)))
    
    # Display payoff breakdown for selected periods
    for period in range(periods_to_view[0], periods_to_view[1] + 1):
        st.markdown(f"### t = {period}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Total Payoff Earned**")
            period_payoffs = pd.DataFrame({
                "Automaton": automatons,
                "Total Payoff": [payoff_history[auto][period] for auto in automatons]
            }).sort_values("Total Payoff", ascending=False)
            st.dataframe(period_payoffs, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Best Response Strategy**")
            period_strategies = strategy_history[period]
            strategy_df = pd.DataFrame({
                "Automaton": list(period_strategies.keys()),
                "Plays Best Against": list(period_strategies.values())
            })
            st.dataframe(strategy_df, use_container_width=True, hide_index=True)
        
        st.markdown("**Pairwise Payoffs (Each automaton vs each opponent)**")
        pairwise_matrix = pairwise_payoffs_history[period]
        st.dataframe(pairwise_matrix.round(4), use_container_width=True)
    
    st.divider()
    st.subheader("📈 Full Payoff Matrix Timeline")
    
    # Create combined payoff matrix for all periods
    combined_payoff_df = pd.concat(payoff_matrices, axis=1)
    st.dataframe(combined_payoff_df.round(4), use_container_width=True)
    
    st.divider()
    st.subheader("🎯 Strategy Selection by Period")
    
    # Create strategy timeline
    strategy_timeline_data = {f"t={period}": strategy_history[period] for period in range(len(strategy_history))}
    strategy_timeline_df = pd.DataFrame(strategy_timeline_data).T
    strategy_timeline_df.index.name = "Time"
    
    st.dataframe(strategy_timeline_df, use_container_width=True)

st.markdown("[🔗 View on Streamlit Sharing](https://github.com/amaanib/Replication-Game)")
