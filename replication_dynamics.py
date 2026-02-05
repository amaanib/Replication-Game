import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

# Set page config
st.set_page_config(
    page_title="Replication Dynamics Game",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader-custom {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎮 Replication Dynamics Game</div>', unsafe_allow_html=True)

# Define the automatons
automatons = ["DOVE", "HAWK", "GRIM", "TIT-FOR-TAT", "TAT-FOR-TIT", 
              "TWEEDLEDUM", "TWEEDLEDEE", "TWEETYPIE"]

# Payoff matrix from the provided table (reading from the image carefully)
# Format: payoff_matrix[player][opponent] = payoff
payoff_matrix = {
    "DOVE":        {"DOVE": 1,    "HAWK": -0.5, "GRIM": 1,    "TIT-FOR-TAT": 1,    "TAT-FOR-TIT": 1,    "TWEEDLEDUM": 1,    "TWEEDLEDEE": 1,    "TWEETYPIE": -0.5},
    "HAWK":        {"DOVE": 3,    "HAWK": 0,    "GRIM": 0,    "TIT-FOR-TAT": 0,    "TAT-FOR-TIT": 1.5,  "TWEEDLEDUM": 1.5,  "TWEEDLEDEE": 1.5,  "TWEETYPIE": 3},
    "GRIM":        {"DOVE": 2,    "HAWK": 0,    "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 0,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": -1},
    "TIT-FOR-TAT": {"DOVE": 2,    "HAWK": 0,    "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2/3,  "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TAT-FOR-TIT": {"DOVE": -0.5, "HAWK": 0.75, "GRIM": 0,    "TIT-FOR-TAT": 2/3,  "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TWEEDLEDUM":  {"DOVE": 2,    "HAWK": 0.75, "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TWEEDLEDEE":  {"DOVE": 2,    "HAWK": 0.75, "GRIM": 2,    "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
    "TWEETYPIE":   {"DOVE": -0.5, "HAWK": 3,    "GRIM": -1,   "TIT-FOR-TAT": 2,    "TAT-FOR-TIT": 2,    "TWEEDLEDUM": 2,    "TWEEDLEDEE": 2,    "TWEETYPIE": 2},
}

def simulate_replication_dynamics(num_periods=100):
    """
    Simulate replication dynamics where:
    - Each automaton starts with equal probability (1/n)
    - In each period, all automatons play against each other
    - Payoffs determine reweighting: highest gets more weight, lowest gets less
    """
    n_automatons = len(automatons)
    
    # Initial equal probabilities
    probabilities = np.ones(n_automatons) / n_automatons
    
    # Track history
    history = []
    history.append(probabilities.copy())
    
    # Track payoffs for each automaton
    payoff_history = defaultdict(list)
    
    for period in range(num_periods):
        # Calculate payoffs for each automaton in this round
        payoffs = np.zeros(n_automatons)
        
        for i, automaton_i in enumerate(automatons):
            # Each automaton plays against all others weighted by their probabilities
            for j, automaton_j in enumerate(automatons):
                payoffs[i] += payoff_matrix[automaton_i][automaton_j] * probabilities[j]
        
        # Store payoffs
        for i, automaton in enumerate(automatons):
            payoff_history[automaton].append(payoffs[i])
        
        # Reweighting based on payoffs
        # Normalize payoffs to be positive (add constant if needed)
        min_payoff = np.min(payoffs)
        if min_payoff < 0:
            payoffs_adjusted = payoffs - min_payoff + 1
        else:
            payoffs_adjusted = payoffs + 1
        
        # Update probabilities proportional to payoffs
        probabilities = probabilities * payoffs_adjusted
        probabilities = probabilities / np.sum(probabilities)
        
        history.append(probabilities.copy())
    
    return np.array(history), payoff_history

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## Settings")
        num_periods = st.slider("Simulation Periods", min_value=10, max_value=200, value=100, step=10)
        
        st.markdown("---")
        st.markdown("### About")
        st.write("""
        This simulation models **replication dynamics** in a game theory setting 
        with 8 different strategies (automatons).
        
        **How it works:**
        - 8 automatons start with equal probability (1/8 each)
        - Each period, they interact weighted by their current probabilities
        - Payoffs determine reweighting: higher payoffs → higher probability
        - Over time, successful strategies prosper
        """)

    # Main content
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 Total Strategies: 8")
    with col2:
        st.info("⏱️ Starting Distribution: 1/8 each")
    with col3:
        st.info("🔄 Dynamic Reweighting: Payoff-based")

    st.markdown("---")

    # Run simulation button
    if st.button("🎮 Run Simulation", use_container_width=True, key="run_button"):
        with st.spinner("Running simulation..."):
            history, payoff_history = simulate_replication_dynamics(num_periods)
        
        # Store in session state
        st.session_state.history = history
        st.session_state.payoff_history = payoff_history
        st.session_state.simulation_run = True

    # Display results if simulation has been run
    if hasattr(st.session_state, 'simulation_run') and st.session_state.simulation_run:
        history = st.session_state.history
        payoff_history = st.session_state.payoff_history
        final_probs = history[-1]
        
        # Summary metrics
        st.markdown('<div class="subheader-custom">📈 Final Results</div>', unsafe_allow_html=True)
        
        final_df = pd.DataFrame({
            "Automaton": automatons,
            "Probability": final_probs,
            "Percentage": final_probs * 100
        }).sort_values("Probability", ascending=False)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_strategy = final_df.iloc[0]
            st.metric("🏆 Most Dominant", top_strategy["Automaton"], 
                     f"{top_strategy['Percentage']:.2f}%")
        
        with col2:
            bottom_strategy = final_df.iloc[-1]
            st.metric("📉 Least Common", bottom_strategy["Automaton"], 
                     f"{bottom_strategy['Percentage']:.2f}%")
        
        with col3:
            herfindahl = np.sum(final_probs ** 2)
            st.metric("🎯 Concentration", f"{herfindahl:.3f}", 
                     "Higher = more concentrated")
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Final Distribution")
            fig_pie = px.pie(
                final_df,
                values="Probability",
                names="Automaton",
                title="Strategy Distribution After Simulation"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### Final Probabilities")
            st.dataframe(final_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Evolution chart
        st.markdown("### Strategy Evolution Over Time")
        
        evolution_df = pd.DataFrame(history, columns=automatons)
        evolution_df['Period'] = range(len(history))
        
        fig_evolution = go.Figure()
        
        colors = px.colors.qualitative.Set2
        for idx, automaton in enumerate(automatons):
            fig_evolution.add_trace(go.Scatter(
                x=evolution_df['Period'],
                y=evolution_df[automaton],
                mode='lines',
                name=automaton,
                stackgroup='one',
                fillcolor=colors[idx % len(colors)]
            ))
        
        fig_evolution.update_layout(
            title="Probability Evolution (Stacked Area)",
            xaxis_title="Period",
            yaxis_title="Probability",
            hovermode='x unified',
            height=450,
            plot_bgcolor="rgba(240, 240, 240, 0.5)"
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        st.markdown("---")
        
        # Payoff evolution
        st.markdown("### Average Payoffs Over Time")
        
        payoff_df = pd.DataFrame(payoff_history)
        payoff_df['Period'] = range(len(payoff_df))
        
        fig_payoff = go.Figure()
        
        for idx, automaton in enumerate(automatons):
            fig_payoff.add_trace(go.Scatter(
                x=payoff_df['Period'],
                y=payoff_df[automaton],
                mode='lines+markers',
                name=automaton,
                line=dict(width=2)
            ))
        
        fig_payoff.update_layout(
            title="Payoff Evolution",
            xaxis_title="Period",
            yaxis_title="Average Payoff",
            hovermode='x unified',
            height=450,
            plot_bgcolor="rgba(240, 240, 240, 0.5)"
        )
        
        st.plotly_chart(fig_payoff, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed results table
        st.markdown("### Detailed Final Results")
        detailed_df = final_df.copy()
        detailed_df["Rank"] = range(1, len(detailed_df) + 1)
        detailed_df = detailed_df[["Rank", "Automaton", "Percentage", "Probability"]]
        detailed_df["Percentage"] = detailed_df["Percentage"].apply(lambda x: f"{x:.2f}%")
        detailed_df["Probability"] = detailed_df["Probability"].apply(lambda x: f"{x:.4f}")
        
        st.dataframe(detailed_df, use_container_width=True, hide_index=True)
    else:
        st.info("👈 Click **Run Simulation** to start the game!")

if __name__ == "__main__":
    main()
