import api from './api';

export const login = async (employeeId, password) => {
  try {
    const response = await api.post('/api/auth/login', {
      employee_id: employeeId,
      password: password
    });
    
    const { access_token, role, employee_id } = response.data;
    
    // Save credentials to local storage securely
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user_role', role);
    localStorage.setItem('employee_id', employee_id);
    
    return { success: true, role };
  } catch (error) {
    console.error("Login failed:", error);
    return { success: false, error: error.response?.data?.detail || "Login failed" };
  }
};

export const logout = () => {
  // Wipe the session data and redirect to login
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_role');
  localStorage.removeItem('employee_id');
  window.location.href = '/'; // Adjust based on your login route
};