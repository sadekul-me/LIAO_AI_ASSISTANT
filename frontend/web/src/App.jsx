// App.jsx

import MainLayout from "./components/layout/MainLayout";
import { AuthProvider } from "./context/AuthContext";


const App = () => {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
};

export default App;