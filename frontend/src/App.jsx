import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Promptbar from './component/Promptbar';
import Circle from './component/Circle';
import { useEffect, useState } from 'react';
import Welcome from './component/Welcome';

function App() {
  const [showWelcome, setShowWelcome] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowWelcome(false); 
    }, 5500);

    return () => clearTimeout(timer); 
  }, []);

  const router = createBrowserRouter([
    {
      path: '/',
      element: (
        <div className='app-container'>
          <Circle />
          <Promptbar />
        </div>
      )
    }
  ]);

  return (
    <div>
      {showWelcome ? <Welcome /> : <RouterProvider router={router} />}
    </div>
  );
}

export default App;
