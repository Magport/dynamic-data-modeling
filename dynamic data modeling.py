import numpy as np
import matplotlib.pyplot as plt

def calculate_cumulative_stats(lambda_rate, time_period, size_mean, size_std, alpha, m, r, i, d, step_size=0.1):
    # Update time_period to reflect the new observation unit
    num_steps = int(time_period / step_size)
    
    # Initialize variables
    arrival_counts = np.random.poisson(lambda_rate * step_size, size=num_steps)
    print("Arrival counts:", arrival_counts)
    sizes = [np.random.normal(size_mean, size_std, size=arrival_counts[t]) for t in range(num_steps)]
    print("Sizes:", sizes)

    # Calculate the total volume of objects at each time step
    total_volumes = np.array([np.sum(sizes[t]) for t in range(num_steps)])

    # Initialize results
    frequencies = np.zeros(num_steps)
    average_sizes = np.zeros(num_steps)
    size_change_rates = np.zeros(num_steps)
    dynamic_blocktimes = np.zeros(num_steps)

    # Calculate the cumulative state from 1 second onwards
    for t in range(num_steps):
        # Total number of objects and total volume from 0 to the current time point
        n = np.sum(arrival_counts[:t+1])
        V_total = np.sum(total_volumes[:t+1])
        
        # Calculate frequency and average size
        frequencies[t] = n / ((t + 1) * step_size)
        average_sizes[t] = V_total / n if n > 0 else 0
        
        # Calculate the rate of change in object size
        all_sizes = np.concatenate(sizes[:t+1])  # All sizes from step 0 to step t
        size_changes = all_sizes[1:] - all_sizes[:-1]  # Calculate the change
        size_change_rates[t] = np.mean(size_changes) if len(size_changes) > 0 else 0  # Calculate average change rate
        
        # Calculate dynamic block time interval D
        Frequency = frequencies[t]
        AverageSize = average_sizes[t]
        SizeChangeRate = size_change_rates[t]
        D = ((alpha * m * d) / i + r * i) / (Frequency + AverageSize + SizeChangeRate)
        dynamic_blocktimes[t] = D
        
        # If the calculated dynamic block time is less than t, record the time and print V_total and V_total/m
        if D < (t + 1) * step_size:
            print(f"At time {(t + 1) * step_size:.1f} seconds, D < t: D = {D:.2f}, V_total = {V_total:.2f}, V_total/m = {V_total/m:.2f}")
        
        # When (t + 1) * step_size == d, record and print V_total and V_total/m
        if (t + 1) * step_size == d:
            print(f"At time {(t + 1) * step_size:.1f} seconds, t = d: V_total = {V_total:.2f}, V_total/m = {V_total/m:.2f}")

    # Print results
    print("Time\tCumulative Frequency (objects/sec)\tCumulative Average Size (units)\tCumulative Size Change Rate (units/sec)\tDynamic Block Time (sec)")
    for t in range(num_steps):
        print(f"Time {(t + 1) * step_size:.1f}: Cumulative Frequency = {frequencies[t]:.2f}, Cumulative Average Size = {average_sizes[t]:.2f}, Cumulative Size Change Rate = {size_change_rates[t]:.2f}, Dynamic Block Time = {dynamic_blocktimes[t]:.2f}")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(step_size, time_period + step_size, step_size), dynamic_blocktimes, marker='o', linestyle='-', color='b')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Dynamic Block Time (seconds)')
    plt.title('Dynamic Block Time over Time')
    plt.grid(True)
    plt.show()

# Call the function
calculate_cumulative_stats(
    lambda_rate=5, 
    time_period=10, 
    size_mean=10, 
    size_std=2, 
    alpha=0.25,   # Ideal block space ratio
    m=1000,      # Maximum block capacity
    r=0.1,       # Ideal transaction change rate
    i=15,        # Ideal number of transactions per block
    d=6,         # Ideal block interval time
    step_size=0.5 # Observation unit of 0.5 seconds
)
