import React from 'react';
import { Link } from 'react-router-dom';
import { Trees as Tree, UserCircle } from 'lucide-react';
import AuthButtons from './auth/AuthButtons';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <Tree className="h-8 w-8 text-green-600" />
              <span className="ml-2 text-xl font-semibold text-gray-900">FamilyTree</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <AuthButtons />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;