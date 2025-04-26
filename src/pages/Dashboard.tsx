import React from 'react';
import { Search, Users, GitBranch, Share2 } from 'lucide-react';

const Dashboard = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Tableau de bord</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <Users className="h-6 w-6 text-green-600 mr-2" />
            <h2 className="text-xl font-semibold">Membres de la famille</h2>
          </div>
          <p className="text-3xl font-bold text-gray-900">24</p>
          <p className="text-sm text-gray-500">personnes dans l'arbre</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <GitBranch className="h-6 w-6 text-green-600 mr-2" />
            <h2 className="text-xl font-semibold">Générations</h2>
          </div>
          <p className="text-3xl font-bold text-gray-900">4</p>
          <p className="text-sm text-gray-500">niveaux de génération</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <Share2 className="h-6 w-6 text-green-600 mr-2" />
            <h2 className="text-xl font-semibold">Partages</h2>
          </div>
          <p className="text-3xl font-bold text-gray-900">8</p>
          <p className="text-sm text-gray-500">membres connectés</p>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <div className="flex items-center mb-6">
          <Search className="h-6 w-6 text-green-600 mr-2" />
          <h2 className="text-xl font-semibold">Rechercher dans l'arbre</h2>
        </div>
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Rechercher un membre..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
          />
          <button className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">
            Rechercher
          </button>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-6">Activités récentes</h2>
        <div className="space-y-4">
          {[
            { action: 'Ajout', person: 'Marie Dupont', date: '2024-02-28' },
            { action: 'Modification', person: 'Jean Martin', date: '2024-02-27' },
            { action: 'Partage', person: 'Famille Martin', date: '2024-02-26' },
          ].map((activity, index) => (
            <div key={index} className="flex items-center justify-between py-2 border-b border-gray-200">
              <div>
                <span className="font-medium">{activity.action}</span>
                <span className="text-gray-600"> - {activity.person}</span>
              </div>
              <span className="text-sm text-gray-500">{activity.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;