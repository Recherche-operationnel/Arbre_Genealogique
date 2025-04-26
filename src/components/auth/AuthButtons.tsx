import React from 'react';
import { Link } from 'react-router-dom';
import { LogIn, UserPlus } from 'lucide-react';

const AuthButtons = () => {
  return (
    <div className="flex space-x-4">
      <Link
        to="/login"
        className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
      >
        <LogIn className="h-5 w-5 mr-1" />
        Connexion
      </Link>
      <Link
        to="/register"
        className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
      >
        <UserPlus className="h-5 w-5 mr-1" />
        S'inscrire
      </Link>
    </div>
  );
};

export default AuthButtons;