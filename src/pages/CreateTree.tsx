import React, { useState, useEffect, useRef } from 'react';
import { Plus, Users, UserPlus, Heart } from 'lucide-react';
import * as go from 'gojs';

interface FamilyMember {
  key: string;
  name: string;
  photo: string;
  gender: string;
  birthDate: string;
}

interface Relationship {
  from: string;
  to: string;
  relationship: 'spouse' | 'child';
}

const CreateTree = () => {
  const diagramRef = useRef<go.Diagram | null>(null);
  const [familyMembers, setFamilyMembers] = useState<FamilyMember[]>([
    { key: '1', name: 'Jean Dupont', photo: 'https://images.unsplash.com/photo-1547425260-76bcadfb4f2c', gender: 'M', birthDate: '1960-05-15' },
    { key: '2', name: 'Marie Dupont', photo: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2', gender: 'F', birthDate: '1962-03-20' },
    { key: '3', name: 'Pierre Dupont', photo: 'https://images.unsplash.com/photo-1566492031773-4f4e44671857', gender: 'M', birthDate: '1985-08-10' },
  ]);

  const [relationships] = useState<Relationship[]>([
    { from: '1', to: '2', relationship: 'spouse' },
    { from: '1', to: '3', relationship: 'child' },
    { from: '2', to: '3', relationship: 'child' },
  ]);

  const [personForm, setPersonForm] = useState({
    firstName: '',
    lastName: '',
    birthDate: '',
    photo: '',
    gender: 'M',
    parent1: '',
    parent2: '',
    spouse: '',
  });

  useEffect(() => {
    if (!diagramRef.current) {
      const $ = go.GraphObject.make;
      
      const diagram = $(go.Diagram, "familyTreeDiagram", {
        initialContentAlignment: go.Spot.Center,
        "undoManager.isEnabled": true,
        layout: $(go.TreeLayout, {
          angle: 90,
          nodeSpacing: 50,
          layerSpacing: 80,
        }),
      });

      // Node template for family members
      diagram.nodeTemplate = $(
        go.Node, "Vertical",
        {
          selectionAdorned: true,
          cursor: "pointer",
          padding: 10,
          background: "#f2f2f2",
        },
        $(
          go.Panel, "Spot", { isClipping: true },
          $(
            go.Shape, "Circle",
            {
              fill: "white",
              stroke: "#4CAF50",
              strokeWidth: 2,
            }
          ),
          $(
            go.Picture,
            {
              width: 100,
              height: 100,
              margin: 10,
            },
            new go.Binding("source", "photo")
          )
        ),
        $(
          go.TextBlock,
          {
            margin: 8,
            font: "bold 14px sans-serif",
          },
          new go.Binding("text", "name")
        )
      );

      // Link template for relationships
      diagram.linkTemplate = $(
        go.Link,
        {
          routing: go.Link.Orthogonal,
          corner: 10,
          layerName: "Background",
        },
        $(go.Shape, { strokeWidth: 2, stroke: "#4CAF50" }),
        $(go.Shape, { toArrow: "Standard", stroke: "#4CAF50", fill: "#4CAF50" })
      );

      diagramRef.current = diagram;
      
      // Initial diagram data
      const nodeDataArray = familyMembers;
      const linkDataArray = relationships.map(rel => ({
        from: rel.from,
        to: rel.to,
      }));

      diagram.model = new go.GraphLinksModel(nodeDataArray, linkDataArray);
    }
  }, [familyMembers, relationships]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newMember: FamilyMember = {
      key: (familyMembers.length + 1).toString(),
      name: `${personForm.firstName} ${personForm.lastName}`,
      photo: personForm.photo || `https://ui-avatars.com/api/?name=${personForm.firstName}+${personForm.lastName}&background=random`,
      gender: personForm.gender,
      birthDate: personForm.birthDate,
    };

    setFamilyMembers([...familyMembers, newMember]);
    setPersonForm({
      firstName: '',
      lastName: '',
      birthDate: '',
      photo: '',
      gender: 'M',
      parent1: '',
      parent2: '',
      spouse: '',
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Créer un arbre généalogique</h1>
          
          <div className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <UserPlus className="h-5 w-5 mr-2 text-green-600" />
              Ajouter une personne
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                    Prénom
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    value={personForm.firstName}
                    onChange={(e) => setPersonForm({ ...personForm, firstName: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                    Nom
                  </label>
                  <input
                    type="text"
                    id="lastName"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    value={personForm.lastName}
                    onChange={(e) => setPersonForm({ ...personForm, lastName: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="birthDate" className="block text-sm font-medium text-gray-700 mb-1">
                    Date de naissance
                  </label>
                  <input
                    type="date"
                    id="birthDate"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    value={personForm.birthDate}
                    onChange={(e) => setPersonForm({ ...personForm, birthDate: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-1">
                    Genre
                  </label>
                  <select
                    id="gender"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    value={personForm.gender}
                    onChange={(e) => setPersonForm({ ...personForm, gender: e.target.value })}
                  >
                    <option value="M">Homme</option>
                    <option value="F">Femme</option>
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="photo" className="block text-sm font-medium text-gray-700 mb-1">
                  Photo (URL)
                </label>
                <input
                  type="url"
                  id="photo"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={personForm.photo}
                  onChange={(e) => setPersonForm({ ...personForm, photo: e.target.value })}
                  placeholder="https://example.com/photo.jpg"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="parent1" className="block text-sm font-medium text-gray-700 mb-1">
                    Parent 1
                  </label>
                  <select
                    id="parent1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    value={personForm.parent1}
                    onChange={(e) => setPersonForm({ ...personForm, parent1: e.target.value })}
                  >
                    <option value="">Sélectionner un parent</option>
                    {familyMembers.map(member => (
                      <option key={member.key} value={member.key}>{member.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label htmlFor="parent2" className="block text-sm font-medium text-gray-700 mb-1">
                    Parent 2
                  </label>
                  <select
                    id="parent2"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    value={personForm.parent2}
                    onChange={(e) => setPersonForm({ ...personForm, parent2: e.target.value })}
                  >
                    <option value="">Sélectionner un parent</option>
                    {familyMembers.map(member => (
                      <option key={member.key} value={member.key}>{member.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="spouse" className="block text-sm font-medium text-gray-700 mb-1">
                  Conjoint(e)
                </label>
                <select
                  id="spouse"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  value={personForm.spouse}
                  onChange={(e) => setPersonForm({ ...personForm, spouse: e.target.value })}
                >
                  <option value="">Sélectionner un(e) conjoint(e)</option>
                  {familyMembers.map(member => (
                    <option key={member.key} value={member.key}>{member.name}</option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors flex items-center justify-center"
              >
                <Plus className="h-5 w-5 mr-2" />
                Ajouter la personne
              </button>
            </form>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Users className="h-5 w-5 mr-2 text-green-600" />
              Membres de la famille
            </h2>
            <div className="space-y-2">
              {familyMembers.map(member => (
                <div key={member.key} className="flex items-center p-2 border-b border-gray-200">
                  <img
                    src={member.photo}
                    alt={member.name}
                    className="w-10 h-10 rounded-full object-cover mr-3"
                  />
                  <div>
                    <p className="font-medium">{member.name}</p>
                    <p className="text-sm text-gray-500">Né(e) le {new Date(member.birthDate).toLocaleDateString()}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div>
          <div className="bg-white p-6 rounded-lg shadow-md" style={{ height: '800px' }}>
            <div id="familyTreeDiagram" style={{ width: '100%', height: '100%', backgroundColor: '#ffffff' }}>
              {/* GoJS diagram is rendered here */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateTree;