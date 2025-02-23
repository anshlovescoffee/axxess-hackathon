import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [activeSection, setActiveSection] = useState('home');
  const [data, setData] = useState(null);

  useEffect(() => {
    if (activeSection !== 'home') {
      axios.get(`http://127.0.0.1:5000/${activeSection}`)
        .then(response => setData(response.data))
        .catch(error => console.error("Error fetching data:", error));
    } else {
      setData(null);
    }
  }, [activeSection]);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-1/4 bg-gray-800 text-white p-4 flex flex-col gap-4">
        <button 
          className={`p-2 rounded ${activeSection === 'patients' ? 'bg-gray-600' : 'bg-gray-700 hover:bg-gray-600'}`} 
          onClick={() => setActiveSection('patients')}
        >
          Patients
        </button>
        <button 
          className={`p-2 rounded ${activeSection === 'inventory' ? 'bg-gray-600' : 'bg-gray-700 hover:bg-gray-600'}`} 
          onClick={() => setActiveSection('inventory')}
        >
          Inventory Management
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-gray-100 p-6">
        <h1 className="text-2xl font-bold">
          {activeSection === 'home' ? 'Welcome to Hospice Management' : `${activeSection.charAt(0).toUpperCase() + activeSection.slice(1)} Section`}
        </h1>
        <div className="mt-4">
          {data ? (
            <div className="bg-white p-4 rounded shadow-md">
              <pre className="whitespace-pre-wrap break-words text-gray-800">{JSON.stringify(data, null, 2)}</pre>
            </div>
          ) : (
            <p className="text-gray-600">Select a section to view data.</p>
          )}
        </div>
      </div>
    </div>
  );
}
