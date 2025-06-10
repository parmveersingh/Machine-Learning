#main-form {
    background-color: #97c2fc47;
    padding: 20px;
    border-radius: 10px;
    z-index: 99999;
}

.cytoscape-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

#cytoscape {
    position: relative;
    overflow: hidden;
    width: 100% !important;
    height: 100% !important;
}

#graph-container[style*="display: block;"] {
    display: flex !important;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 90vh;
}

#layout-controls {
    display: none;
}

#graph-container[style*="display: block;"] {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 90vh;
}

#button-container {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

#search-type-dropdown, .dash-dropdown {
    padding: 12px 0px;
}

.dash-input {
    width: 94%;
    font-family: inherit;
    line-height: 34px;
    padding-left: 10px;
    padding-right: 10px;
    margin: 12px 0px;
    font-size: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

#reset-button, #search-button {
    background-color: #c1ffd861;
    border-radius: 100px;
    box-shadow: rgba(44, 187, 99, .2) 0 -25px 18px -14px inset, 
                rgba(44, 187, 99, .15) 0 1px 2px, 
                rgba(44, 187, 99, .15) 0 2px 4px, 
                rgba(44, 187, 99, .15) 0 4px 8px, 
                rgba(44, 187, 99, .15) 0 8px 16px, 
                rgba(44, 187, 99, .15) 0 16px 32px;
    color: green;
    cursor: pointer;
    flex: 1;
    margin: 0 5px;
    padding: 7px 20px;
    text-align: center;
    text-decoration: none;
    transition: all 250ms;
    border: 0;
    font-size: 16px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#search-button {
    margin-right: 10px;
}

#search-status {
    font-family: inherit;
    margin: 12px 0px;
    color: #ca4545;
}

input, select {
    background-color: #FFFFFF !important;
}

#zoom-slider {
    padding: 12px 0px 25px 10px !important;
}

#layout-dropdown .Select-menu-outer {
    overflow: scroll;
    height: 100px;
}

#cytoscape {
    width: 100% !important;
    height: 100% !important;
}
