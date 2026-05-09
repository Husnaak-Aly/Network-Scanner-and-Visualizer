document.addEventListener('DOMContentLoaded', function() {
    const loadingEl = document.getElementById('loading');
    const infoEl = document.getElementById('info');

    fetch('data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            loadingEl.style.display = 'none'; // Hide loading message

            if (!data || !data.nodes || data.nodes.length === 0) {
                loadingEl.innerText = 'No devices found. Ensure scanner.py ran correctly.';
                loadingEl.style.display = 'block';
                return;
            }

            var cy = cytoscape({
                container: document.getElementById('cy'),
                elements: data,
                style: [
                    { selector: 'node', style: {
                        'label': 'data(label)', 'color': '#fff', 'text-valign': 'center',
                        'text-halign': 'center', 'font-size': '10px', 'text-wrap': 'wrap',
                        'text-outline-width': 2, 'text-outline-color': '#888', 'width': '60px', 'height': '60px'
                    }},
                    { selector: 'edge', style: {
                        'width': 2, 'line-color': '#ccc', 'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle', 'curve-style': 'bezier'
                    }},
                    // --- Custom Node Styles ---
                    { selector: 'node[type = "router"]', style: {'background-color': '#e67e22', 'shape': 'diamond'}},
                    { selector: 'node[type = "windows"]', style: {'background-color': '#3498db', 'shape': 'rectangle'}},
                    { selector: 'node[type = "linux"]', style: {'background-color': '#c0392b'}},
                    { selector: 'node[type = "mac"]', style: {'background-color': '#bdc3c7'}},
                    { selector: 'node[type = "web-server"]', style: {'background-color': '#27ae60', 'shape': 'triangle'}},
                    { selector: 'node[type = "host"]', style: {'background-color': '#95a5a6'}},
                    // Style for selected nodes
                    { selector: ':selected', style: {
                        'border-width': 3, 'border-color': '#333'
                    }}
                ],
                layout: {
                    name: 'cose',
                    idealEdgeLength: 150,
                    nodeRepulsion: 500000,
                    fit: true,
                    padding: 50
                }
            });

            // --- Interactivity ---
            cy.on('tap', 'node', function(evt){
                var node = evt.target;
                var data = node.data();
                
                // Build the HTML for the info panel
                let portsHtml = '<strong>No open ports found.</strong>';
                if (data.ports && data.ports.length > 0) {
                    portsHtml = `<strong>Open Ports:</strong><ul id="ports-list">`;
                    data.ports.forEach(port => {
                        portsHtml += `<li>${port.portid}/${port.protocol} - ${port.service}</li>`;
                    });
                    portsHtml += `</ul>`;
                }

                infoEl.innerHTML = `
                    <h2>${data.id}</h2>
                    <p><strong>Type:</strong> ${data.type.charAt(0).toUpperCase() + data.type.slice(1)}</p>
                    <p><strong>OS Guess:</strong> ${data.os}</p>
                    <hr>
                    ${portsHtml}
                `;
                infoEl.classList.add('visible'); // Show the panel
            });

            // Tap on the background to hide the info panel
            cy.on('tap', function(evt){
                if (evt.target === cy) {
                    infoEl.classList.remove('visible');
                }
            });

        })
        .catch(error => {
            console.error('Error loading or processing graph data:', error);
            loadingEl.innerText = 'Error: Could not load data.json. Did you run the scanner?';
            loadingEl.style.display = 'block';
        });
});
