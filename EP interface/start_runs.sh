#!/bin/zsh

# Define scenarios folder and scenario name
scenarios_folder="/Users//Documents/EnergyPATHWAYS/model_runs"
scenario_name="test_scenario"

# Change the working directory to scenarios_folder/scenario_name
cd "${scenarios_folder}/${scenario_name}" || exit 1

# Assuming these are the inputs we would get from Excel, hardcoded for the example
ep_load_demand=false
ep_export_results=true
ep_save_models=true
scenario_list=("reference" "eplus" "eplus reduce exports" "eminus") # Example scenario names

# Convert the Excel true/false to command line flags
load_demand_flag="--no_load_demand"
if [ "$ep_load_demand" = true ]; then
    load_demand_flag="--load_demand"
fi

export_results_flag=""
if [ "$ep_export_results" = false ]; then
    export_results_flag="--no_export_results"
fi

save_models_flag=""
if [ "$ep_save_models" = false ]; then
    save_models_flag="--no_save_models"
fi

# Common parameters for all scenarios
params="${load_demand_flag} ${export_results_flag} ${save_models_flag}"

# Maximum number of parallel jobs
MAX_JOBS=2

# Use an array to keep track of job PIDs
declare -a job_pids

first_scenario=true

# Loop through the scenarios and execute the command in background
for scenario in "${scenario_list[@]}"; do
    # Determine the shape_owner_flag based on whether it's the first scenario
    if [ "$first_scenario" = true ]; then
        shape_owner_flag="--shape_owner"
        first_scenario=false # Ensure this block only runs once
    else
        shape_owner_flag="--no_shape_owner"
    fi
    
    # Construct the command with current scenario
    command="energyPATHWAYS -s \"$scenario\" $params $shape_owner_flag"
    
    # Execute the command in the background
    echo "Executing in background: $command"
    eval "$command" &
    job_pids+=($!)
    
    # Job management to ensure we do not exceed MAX_JOBS
    while [ ${#job_pids[@]} -ge $MAX_JOBS ]; do
        # Temporary array to hold jobs still running
        still_running=()
        for pid in "${job_pids[@]}"; do
            if kill -0 $pid 2>/dev/null; then
                # Job is still running, add it to the still_running array
                still_running+=($pid)
            fi
        done
        # Update the job_pids array to only include jobs that are still running
        job_pids=("${still_running[@]}")
        # If we are at or above the job limit, sleep before checking again
        if [ ${#job_pids[@]} -ge $MAX_JOBS ]; then
            sleep 1
        fi
    done
done

# Wait for the last batch of jobs to complete
wait

echo "All scenarios have been executed with a maximum of $MAX_JOBS in parallel."