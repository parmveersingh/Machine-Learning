/* Add these styles to your existing CSS */

.dropdown-menu {
    border: none;
    border-radius: 8px;
    box-shadow: var(--card-shadow);
    padding: 0.5rem;
    margin-top: 0.5rem;
    width: 100%; /* Ensure full width */
    max-height: 300px; /* Fixed height for scrolling */
    overflow-y: auto; /* Enable scrolling */
    overflow-x: hidden; /* Prevent horizontal scroll */
}

.search-input {
    border: 2px solid #e9ecef;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    width: calc(100% - 1rem); /* Account for margin */
    margin-left: 0.5rem;
    margin-right: 0.5rem;
}

.search-input:focus {
    border-color: var(--secondary-color);
    box-shadow: none;
    outline: none;
}

.dropdown-list-container {
    max-height: 250px; /* Space for search input + items */
    overflow-y: auto;
}

.dropdown-item {
    padding: 0.75rem 1rem;
    border-radius: 6px;
    margin-bottom: 0.25rem;
    transition: all 0.2s ease;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
}

.dropdown-item:hover {
    background-color: var(--secondary-color);
    color: white;
}

.no-results {
    padding: 0.75rem 1rem;
    color: #6c757d;
    font-style: italic;
    text-align: center;
}

/* Ensure dropdown toggle shows full text */
.dropdown-toggle {
    width: 100%;
    text-align: left;
    padding: 0.75rem 1rem;
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: space-between;
    overflow: hidden;
}

.dropdown-toggle-text {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
}