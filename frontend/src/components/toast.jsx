// src/components/Toast.jsx
import { Toaster } from "react-hot-toast";

const Toast = () => {
  return (
    <Toaster
      position='top-right'
      toastOptions={{
        success: {
          style: {
            background: "#4caf50",
            color: "#fff",
          },
        },
        error: {
          style: {
            background: "#f44336",
            color: "#fff",
          },
        },
      }}
    />
  );
};

export default Toast;
