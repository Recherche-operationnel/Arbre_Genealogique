import { useState } from 'react'
import { FiEdit2, FiPlusCircle, FiImage } from 'react-icons/fi'
import './App.css'

function App() {
  const [familyTree, setFamilyTree] = useState({
    id: 1,
    nom: 'Grand-Père',
    genre: 'homme',
    dateNaissance: '1920-01-01',
    photo: '',
    conjoint: {
      id: 2,
      nom: 'Grand-Mère',
      genre: 'femme',
      dateNaissance: '1922-01-01',
      photo: ''
    }
  })

  const [editingPerson, setEditingPerson] = useState(null)
  const [addingChild, setAddingChild] = useState(null)
  const [addingConjoint, setAddingConjoint] = useState(null)
  const [tempPhoto, setTempPhoto] = useState(null)

  const findPersonInTree = (tree, id) => {
    if (tree.id === id) return tree
    if (tree.conjoint?.id === id) return tree.conjoint
    if (tree.enfants) {
      for (const child of tree.enfants) {
        const found = findPersonInTree(child, id)
        if (found) return found
      }
    }
    return null
  }

  const findParentsInTree = (tree, childId, parents = null) => {
    if (tree.enfants) {
      for (const child of tree.enfants) {
        if (child.id === childId) {
          return {
            parent: tree,
            conjoint: tree.conjoint
          }
        }
        const found = findParentsInTree(child, childId)
        if (found) return found
      }
    }
    return null
  }

  const getPersonDetails = (id) => {
    const person = findPersonInTree(familyTree, id)
    const parents = findParentsInTree(familyTree, id)
    return {
      person,
      parents,
      children: person?.enfants || [],
      conjoint: person?.conjoint
    }
  }

  const handleEdit = (person) => {
    const details = getPersonDetails(person.id)
    setEditingPerson({ ...person, ...details })
  }

  const handlePhotoChange = (e, personId) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        if (personId) {
          const updateTreeData = (tree, personId, photoUrl) => {
            if (tree.id === personId) {
              return { ...tree, photo: photoUrl }
            }
            if (tree.conjoint && tree.conjoint.id === personId) {
              return { ...tree, conjoint: { ...tree.conjoint, photo: photoUrl } }
            }
            if (tree.enfants) {
              return {
                ...tree,
                enfants: tree.enfants.map(child => updateTreeData(child, personId, photoUrl))
              }
            }
            return tree
          }
          setFamilyTree(prev => updateTreeData(prev, personId, reader.result))
        } else {
          setTempPhoto(reader.result)
        }
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSave = (e) => {
    e.preventDefault()
    const updateTreeData = (tree, personId, newData) => {
      if (tree.id === personId) {
        return { ...tree, ...newData }
      }
      if (tree.conjoint && tree.conjoint.id === personId) {
        return { ...tree, conjoint: { ...tree.conjoint, ...newData } }
      }
      if (tree.enfants) {
        return {
          ...tree,
          enfants: tree.enfants.map(child => updateTreeData(child, personId, newData))
        }
      }
      return tree
    }

    const formData = {
      nom: e.target.nom.value,
      dateNaissance: e.target.dateNaissance.value,
      dateDeces: e.target.dateDeces.value || null
    }

    setFamilyTree(prev => updateTreeData(prev, editingPerson.id, formData))
    setEditingPerson(null)
  }

  const handleAddChild = (e) => {
    e.preventDefault()
    const newChild = {
      id: Date.now(),
      nom: e.target.nom.value,
      genre: e.target.genre.value,
      dateNaissance: e.target.dateNaissance.value,
      photo: tempPhoto || ''
    }

    const addChildToTree = (tree, parentId) => {
      if (tree.id === parentId) {
        return {
          ...tree,
          enfants: [...(tree.enfants || []), newChild]
        }
      }
      if (tree.enfants) {
        return {
          ...tree,
          enfants: tree.enfants.map(child => addChildToTree(child, parentId))
        }
      }
      return tree
    }

    setFamilyTree(prev => addChildToTree(prev, addingChild.id))
    setAddingChild(null)
    setTempPhoto(null)
  }

  const handleAddConjoint = (e) => {
    e.preventDefault()
    const newConjoint = {
      id: Date.now(),
      nom: e.target.nom.value,
      genre: e.target.genre.value,
      dateNaissance: e.target.dateNaissance.value,
      photo: tempPhoto || ''
    }

    const addConjointToTree = (tree, personId) => {
      if (tree.id === personId) {
        return { ...tree, conjoint: newConjoint }
      }
      if (tree.enfants) {
        return {
          ...tree,
          enfants: tree.enfants.map(child => addConjointToTree(child, personId))
        }
      }
      return tree
    }

    setFamilyTree(prev => addConjointToTree(prev, addingConjoint.id))
    setAddingConjoint(null)
    setTempPhoto(null)
  }

  const PersonCard = ({ person, level }) => {
    const cardStyle = {
      backgroundColor: person.genre === 'homme' ? '#2563eb' : '#db2777',
      color: 'white'
    }

    return (
      <div className={`person-card level-${level}`} style={cardStyle}>
        <div className="card-actions">
          <button className="icon-button" onClick={() => handleEdit(person)}>
            <FiEdit2 />
            <span className="icon-label">Modifier</span>
          </button>
          {!person.conjoint && (
            <button className="icon-button" onClick={() => setAddingConjoint(person)}>
              <FiPlusCircle />
              <span className="icon-label">Conjoint</span>
            </button>
          )}
          <button className="icon-button" onClick={() => setAddingChild(person)}>
            <FiPlusCircle />
            <span className="icon-label">Enfant</span>
          </button>
          <label className="icon-button photo-upload">
            <FiImage />
            <span className="icon-label">Photo</span>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => handlePhotoChange(e, person.id)}
              style={{ display: 'none' }}
            />
          </label>
        </div>
        {person.photo && (
          <div className="photo-container">
            <img src={person.photo} alt={person.nom} className="person-photo" />
          </div>
        )}
        <div className="card-content">
          <h3>{person.nom}</h3>
          <p>Naissance: {new Date(person.dateNaissance).toLocaleDateString()}</p>
          {person.dateDeces && (
            <p>Décès: {new Date(person.dateDeces).toLocaleDateString()}</p>
          )}
        </div>
      </div>
    )
  }

  const FamilyNode = ({ node, level = 0 }) => {
    return (
      <div className={`family-node level-${level}`}>
        <div className="couple">
          <PersonCard person={node} level={level} />
          {node.conjoint && (
            <PersonCard person={node.conjoint} level={level} />
          )}
        </div>
        {node.enfants && node.enfants.length > 0 && (
          <div className="children">
            {node.enfants.map((child, index) => (
              <FamilyNode key={child.id} node={child} level={level + 1} />
            ))}
          </div>
        )}
      </div>
    )
  }

  const PhotoUploadPreview = ({ onChange }) => (
    <label className="photo-upload-preview">
      {tempPhoto ? (
        <img src={tempPhoto} alt="Aperçu" />
      ) : (
        <>
          <FiImage className="photo-upload-icon" />
          <span className="photo-upload-text">Cliquez pour ajouter une photo</span>
        </>
      )}
      <input
        type="file"
        accept="image/*"
        onChange={onChange}
        style={{ display: 'none' }}
      />
    </label>
  )

  return (
    <div className="app" width="100%">
      <h1>Arbre Généalogique</h1>
      <div className="family-tree">
        <FamilyNode node={familyTree} />
      </div>

      {editingPerson && (
        <div className="modal">
          <div className="modal-content">
            <h2>Modifier les informations</h2>
            <form onSubmit={handleSave}>
              <div className="form-section">
                <h3>Informations personnelles</h3>
                <div className="form-group">
                  <label>Nom:</label>
                  <input
                    name="nom"
                    defaultValue={editingPerson.nom}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Date de naissance:</label>
                  <input
                    type="date"
                    name="dateNaissance"
                    defaultValue={editingPerson.dateNaissance}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Date de décès:</label>
                  <input
                    type="date"
                    name="dateDeces"
                    defaultValue={editingPerson.dateDeces}
                  />
                </div>
                <div className="form-group">
                  <label>Photo:</label>
                  {editingPerson.photo ? (
                    <div className="edit-photo-preview">
                      <img src={editingPerson.photo} alt={editingPerson.nom} />
                    </div>
                  ) : (
                    <p className="no-info">Aucune photo</p>
                  )}
                </div>
              </div>

              <div className="form-section">
                <h3>Parents</h3>
                {editingPerson.parents ? (
                  <div className="family-info">
                    <p><strong>Parent 1:</strong> {editingPerson.parents.parent.nom}</p>
                    {editingPerson.parents.conjoint && (
                      <p><strong>Parent 2:</strong> {editingPerson.parents.conjoint.nom}</p>
                    )}
                  </div>
                ) : (
                  <p className="no-info">Aucun parent enregistré</p>
                )}
              </div>

              <div className="form-section">
                <h3>Conjoint</h3>
                {editingPerson.conjoint ? (
                  <div className="family-info">
                    <p><strong>Nom:</strong> {editingPerson.conjoint.nom}</p>
                    <p><strong>Naissance:</strong> {new Date(editingPerson.conjoint.dateNaissance).toLocaleDateString()}</p>
                  </div>
                ) : (
                  <p className="no-info">Aucun conjoint enregistré</p>
                )}
              </div>

              <div className="form-section">
                <h3>Enfants</h3>
                {editingPerson.children && editingPerson.children.length > 0 ? (
                  <div className="family-info">
                    {editingPerson.children.map(child => (
                      <div key={child.id} className="child-info">
                        <p><strong>Nom:</strong> {child.nom}</p>
                        <p><strong>Naissance:</strong> {new Date(child.dateNaissance).toLocaleDateString()}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="no-info">Aucun enfant enregistré</p>
                )}
              </div>

              <div className="modal-buttons">
                <button type="submit" className="btn btn-primary">Sauvegarder</button>
                <button type="button" className="btn btn-danger" onClick={() => setEditingPerson(null)}>
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {addingChild && (
        <div className="modal">
          <div className="modal-content">
            <h2>Ajouter un enfant</h2>
            <form onSubmit={handleAddChild}>
              <div className="form-section">
                <div className="form-group">
                  <label>Nom:</label>
                  <input name="nom" required />
                </div>
                <div className="form-group">
                  <label>Genre:</label>
                  <select name="genre" required>
                    <option value="homme">Homme</option>
                    <option value="femme">Femme</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Date de naissance:</label>
                  <input type="date" name="dateNaissance" required />
                </div>
                <div className="form-group">
                  <label>Photo:</label>
                  <PhotoUploadPreview onChange={(e) => handlePhotoChange(e)} />
                </div>
              </div>
              <div className="modal-buttons">
                <button type="submit" className="btn btn-primary">Ajouter</button>
                <button type="button" className="btn btn-danger" onClick={() => {
                  setAddingChild(null)
                  setTempPhoto(null)
                }}>
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {addingConjoint && (
        <div className="modal">
          <div className="modal-content">
            <h2>Ajouter un conjoint</h2>
            <form onSubmit={handleAddConjoint}>
              <div className="form-section">
                <div className="form-group">
                  <label>Nom:</label>
                  <input name="nom" required />
                </div>
                <div className="form-group">
                  <label>Genre:</label>
                  <select name="genre" required>
                    <option value="homme">Homme</option>
                    <option value="femme">Femme</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Date de naissance:</label>
                  <input type="date" name="dateNaissance" required />
                </div>
                <div className="form-group">
                  <label>Photo:</label>
                  <PhotoUploadPreview onChange={(e) => handlePhotoChange(e)} />
                </div>
              </div>
              <div className="modal-buttons">
                <button type="submit" className="btn btn-primary">Ajouter</button>
                <button type="button" className="btn btn-danger" onClick={() => {
                  setAddingConjoint(null)
                  setTempPhoto(null)
                }}>
                  Annuler
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default App