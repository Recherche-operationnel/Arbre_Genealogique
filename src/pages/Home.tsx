import React from 'react';
import { Link } from 'react-router-dom';
import { Trees as Tree, Plus } from 'lucide-react';

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Créez votre arbre généalogique
        </h1>
        <p className="text-xl text-gray-600 mb-12">
          Explorez votre histoire familiale et partagez-la avec vos proches
        </p>
        <Link
          to="/create-tree"
          className="inline-flex items-center px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
        >
          <Plus className="h-5 w-5 mr-2" />
          Créer un arbre
        </Link>
      </div>
      
      <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {/* Feature cards */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Tree className="h-12 w-12 text-green-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Visualisation intuitive</h3>
          <p className="text-gray-600">
            Créez et visualisez votre arbre généalogique avec une interface claire et interactive
          </p>
        </div>
        {/* Add more feature cards as needed */}
      </div>
    </div>
  );
};

export default Home;