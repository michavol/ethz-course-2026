import numpy as np


def generate_quintic_spline_waypoints(
    start: np.ndarray, end: np.ndarray, num_points: int
) -> np.ndarray:
    """Generate trajectory waypoints using quintic time scaling.

    Uses the time-scaling polynomial f(s) = 10s^3 - 15s^4 + 6s^5 to
    interpolate smoothly between the start and end waypoints with zero
    velocity and acceleration at both boundaries.

    Args:
        start: Starting waypoint (shape: dof,).
        end: Ending waypoint (shape: dof,).
        num_points: Number of points in the trajectory.

    Returns:
        Array of waypoints with shape (num_points, dof).
    """
    s = np.linspace(0.0, 1.0, num_points)
    f_s = 10.0 * s**3 - 15.0 * s**4 + 6.0 * s**5
    return start + (end - start) * f_s[:, np.newaxis]


def pid_control(tracking_error_history, timestep, Kp=150.0, Ki=0.0, Kd=0.01):
    """
    TODO:
    Compute the PID control signal based on the tracking error history.
    
    Steps:
    1. The Proportional (P) term is the most recent error.
    2. The Integral (I) term is the sum of all past errors, multiplied by the simulation timestep.
    3. The Derivative (D) term is the rate of change of the error (difference between the last two errors divided by the timestep).
       If there is only one error in history, the D term should be zero.
    4. Compute the final control signal: Kp * P + Ki * I + Kd * D.
    
    Args:
        tracking_error_history (np.ndarray): History of tracking errors.
        timestep (float): Simulation timestep.
        Kp (float): Proportional gain.
        Ki (float): Integral gain.
        Kd (float): Derivative gain.
        
    Returns:
        np.ndarray: Control signal.
    """
    errors = np.asarray(tracking_error_history)

    # Proportional term uses the most recent error.
    e_k = errors[-1]

    # Integral term: sum of all past errors scaled by timestep.
    integral = np.sum(errors, axis=0) * timestep

    # Derivative term: finite difference of the last two errors.
    if errors.shape[0] < 2:
        derivative = np.zeros_like(e_k)
    else:
        e_k_minus_1 = errors[-2]
        derivative = (e_k - e_k_minus_1) / timestep

    return Kp * e_k + Ki * integral + Kd * derivative
            