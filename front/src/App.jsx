import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from './config';
import './App.css'
const App = () => {
  const [products, setProducts] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    description: '',
    category: '',
    price: '',
    sku: '',
  });
  const [transferData, setTransferData] = useState({
    product_id: '',
    source_store_id: '',
    target_store_id: '',
    quantity: 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProducts();
    fetchAlerts();
  }, []);

  const fetchProducts = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/products`);


      console.log({API_BASE_URL})
      console.log(response.data.products)
      setProducts(response.data.products);
      setError(null);
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('Failed to load products.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchInventory = async (storeId) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/stores/${storeId}/inventory`);
      setInventory(response.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching inventory:', error);
      setError('Failed to load inventory.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchAlerts = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/inventory/alerts`);
      setAlerts(response.data.products);
      setError(null);
    } catch (error) {
      console.error('Error fetching alerts:', error);
      setError('Failed to load alerts.');
    } finally {
      setIsLoading(false);
    }
  };

  const createProduct = async () => {
    setIsLoading(true);
    try {
        console.log("Create")
      await axios.post(`${API_BASE_URL}/api/products/`, formData);
        console.log("Create")
      fetchProducts();
      setError(null);
    } catch (error) {
      console.error('Error creating product:', error);
      setError('Failed to create product.');
    } finally {
      setIsLoading(false);
    }
  };

  const updateProduct = async (id) => {
    setIsLoading(true);
    try {
      await axios.put(`${API_BASE_URL}/api/products/${id}`, formData);
      fetchProducts();
      setError(null);
    } catch (error) {
      console.error('Error updating product:', error);
      setError('Failed to update product.');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteProduct = async (id) => {
    setIsLoading(true);
    try {
      await axios.delete(`${API_BASE_URL}/api/products/${id}`);
      fetchProducts();
      setError(null);
    } catch (error) {
      console.error('Error deleting product:', error);
      setError('Failed to delete product.');
    } finally {
      setIsLoading(false);
    }
  };

  const transferInventory = async () => {
    setIsLoading(true);
    try {
      await axios.post(`${API_BASE_URL}/api/inventory/transfer`, transferData);
      fetchInventory(transferData.target_store_id);
      setError(null);
    } catch (error) {
      console.error('Error transferring inventory:', error);
      setError('Failed to transfer inventory.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Inventory Management</h1>

      {error && <p className="error-message">{error}</p>}
      {isLoading && <p className="loading-message">Loading...</p>}

      <section className="section">
        <h2 className="section-title">Products</h2>
        <div className="products-list">
          {products.length > 0 ? (
            products.map((product) => (
              <div className="product-card" key={product.id}>
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <p>Category: {product.category}</p>
                <p>Price: ${product.price}</p>
                <p>SKU: {product.sku}</p>
                <button className="delete-button" onClick={() => deleteProduct(product.id)}>Delete</button>
              </div>
            ))
          ) : (
            <p>No products available.</p>
          )}
        </div>
        <h3>Add / Update Product</h3>
        <input className="input" placeholder="ID" value={formData.id || ''} onChange={(e) => setFormData({ ...formData, id: e.target.value })} />
        <input className="input" placeholder="Name" value={formData.name || ''} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
        <input className="input" placeholder="Description" value={formData.description || ''} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
        <input className="input" placeholder="Category" value={formData.category || ''} onChange={(e) => setFormData({ ...formData, category: e.target.value })} />
        <input className="input" placeholder="Price" value={formData.price || ''} onChange={(e) => setFormData({ ...formData, price: e.target.value })} />
        <input className="input" placeholder="SKU" value={formData.sku || ''} onChange={(e) => setFormData({ ...formData, sku: e.target.value })} />
        <button className="button" onClick={createProduct}>Add</button>
        <button className="button" onClick={() => updateProduct(formData.id)}>Update</button>
      </section>

      <section className="section">
        <h2 className="section-title">Inventory</h2>
        <input className="input" placeholder="ID" value={formData.id || ''} onChange={(e) => setFormData({ ...formData, id: e.target.value })} />
        <button className="button" onClick={() => fetchInventory(formData.id)}>Load Store Inventory</button>
        <div className="inventory-list">
          {inventory.length > 0 ? (
            inventory.map((item) => (
              <div className="inventory-card" key={item.id}>
                <p>Product ID: {item.product_id}</p>
                <p>Store ID: {item.store_id}</p>
                <p>Quantity: {item.quantity}</p>
                <p>Minimum Stock: {item.min_stock}</p>
              </div>
            ))
          ) : (
            <p>No inventory data available.</p>
          )}
        </div>
      </section>

      <section className="section">
        <h2 className="section-title">Low Stock Alerts</h2>
        <div className="alerts-list">
          {alerts.length > 0 ? (
            alerts.map((alert) => (
              <div className="alert-card" key={alert.id}>
                <p>Product ID: {alert.product_id}</p>
                <p>Store ID: {alert.store_id}</p>
                <p>Quantity: {alert.quantity}</p>
                <p>Minimum Stock: {alert.min_stock}</p>
              </div>
            ))
          ) : (
            <p>No alerts available.</p>
          )}
        </div>
      </section>

      <section className="section">
        <h2 className="section-title">Transfer Inventory</h2>
        <input className="input" placeholder="Product ID" value={transferData.product_id || ''} onChange={(e) => setTransferData({ ...transferData, product_id: e.target.value })} />
        <input className="input" placeholder="Source Store ID" value={transferData.source_store_id || ''} onChange={(e) => setTransferData({ ...transferData, source_store_id: e.target.value })} />
        <input className="input" placeholder="Target Store ID" value={transferData.target_store_id || ''} onChange={(e) => setTransferData({ ...transferData, target_store_id: e.target.value })} />
        <input className="input" placeholder="Quantity" type="number" value={transferData.quantity || ''} onChange={(e) => setTransferData({ ...transferData, quantity: e.target.value })} />
        <button className="button" onClick={transferInventory}>Transfer</button>
      </section>
    </div>
  );
};


export default App;
