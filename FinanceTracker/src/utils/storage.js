// Save a value to local storage
export const saveToLocalStorage = (key, value) => {
  localStorage.setItem(key, JSON.stringify(value));  // Store the value as a JSON string
};

// Retrieve a value from local storage
export const getFromLocalStorage = (key) => {
  const data = localStorage.getItem(key);  // Get the JSON string from local storage
  return data ? JSON.parse(data) : [];     // Parse and return the value, or an empty array if not found
};
