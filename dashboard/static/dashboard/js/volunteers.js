    

    let filteredVolunteers = [...volunteers];
    let currentPage = 1;
    let entriesPerPage = 10;
    let sortDirection = 'asc';
    let sortColumn = '';

    // Initialize the dashboard
    function init() {
        displayTable();
        setupEventListeners();
    }

    // Display table with pagination
    function displayTable() {
        const tbody = document.getElementById('volunteerTableBody');
        const startIndex = (currentPage - 1) * entriesPerPage;
        const endIndex = startIndex + entriesPerPage;
        const pageData = filteredVolunteers.slice(startIndex, endIndex);

        tbody.innerHTML = '';

        if (pageData.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="px-6 py-12 text-center text-gray-500">
                        <i class="fas fa-users text-4xl mb-4 text-gray-300"></i>
                        <p class="text-lg font-medium">No volunteers found</p>
                        <p class="text-sm">Try adjusting your search or filters</p>
                    </td>
                </tr>
            `;
            return;
        }

        pageData.forEach((volunteer) => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-gray-50 transition-colors duration-200';

            let actionButton;
            if (volunteer.status == "approved"){
                statusButton = `<button onclick="showSuspendModal('${volunteer.reg_no}')"
                                class="text-yellow-600 hover:text-yellow-900 bg-yellow-50 hover:bg-yellow-100 px-3 py-1 rounded-md transition-colors duration-200">
                                <i class="fas fa-user-slash mr-1"></i>Suspend
                            </button>`;
            }else{
                statusButton = `<button onclick="showReactivateModal('${volunteer.reg_no}')"
                                class="text-green-600 hover:text-green-900 bg-green-50 hover:bg-green-100 px-3 py-1 rounded-md transition-colors duration-200">
                                <i class="fas fa-user-check mr-1"></i>Reactivate
                            </button>`;
            }

            row.innerHTML = `
                <td class="px-4 sm:px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">${volunteer.reg_no}</div>
                </td>
                <td class="px-4 sm:px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 h-8 w-8">
                            <div class="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center">
                                <span class="text-sm font-medium text-gray-700">${volunteer.name.charAt(0)}</span>
                            </div>
                        </div>
                        <div class="ml-3">
                            <div class="text-sm font-medium text-gray-900">${volunteer.name}</div>
                        </div>
                    </div>
                </td>
                <td class="px-4 sm:px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getDesignationColor(volunteer.designation)}">
                        ${volunteer.designation.charAt(0).toUpperCase() + volunteer.designation.slice(1)}
                    </span>
                </td>
                <td class="px-4 sm:px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex flex-col sm:flex-row gap-2">
                        <a href="${EDIT_VOLUNTEER_BASE_URL}${volunteer.reg_no}"
                           class="text-blue-600 hover:text-blue-900 bg-blue-50 hover:bg-blue-100 px-3 py-1 rounded-md transition-colors duration-200 text-center">
                            <i class="fas fa-edit mr-1"></i>Edit
                        </a>
                        <button onclick="showDeleteModal('${volunteer.reg_no}')" 
                                class="text-red-600 hover:text-red-900 bg-red-50 hover:bg-red-100 px-3 py-1 rounded-md transition-colors duration-200">
                            <i class="fas fa-trash mr-1"></i>Delete
                        </button>

                        ${statusButton}

                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });

        updatePagination();
    }

    // Get color class for designation badge
    function getDesignationColor(designation) {
        const colors = {
            'teacher': 'bg-blue-100 text-blue-800',
            'admin': 'bg-purple-100 text-purple-800'
        };
        return colors[designation] || 'bg-gray-100 text-gray-800';
    }

    // Update pagination controls
    function updatePagination() {
        const totalPages = Math.ceil(filteredVolunteers.length / entriesPerPage);
        const startEntry = (currentPage - 1) * entriesPerPage + 1;
        const endEntry = Math.min(currentPage * entriesPerPage, filteredVolunteers.length);

        document.getElementById('showingFrom').textContent = filteredVolunteers.length ? startEntry : 0;
        document.getElementById('showingTo').textContent = endEntry;
        document.getElementById('totalEntries').textContent = filteredVolunteers.length;

        document.getElementById('prevBtn').disabled = currentPage === 1;
        document.getElementById('nextBtn').disabled = currentPage === totalPages || totalPages === 0;

        // Update page numbers
        const pageNumbers = document.getElementById('pageNumbers');
        pageNumbers.innerHTML = '';

        if (totalPages > 0) {
            for (let i = 1; i <= totalPages; i++) {
                if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
                    const button = document.createElement('button');
                    button.textContent = i;
                    button.className = `px-3 py-2 text-sm font-medium border rounded-md ${
                        i === currentPage 
                            ? 'bg-blue-600 text-white border-blue-600' 
                            : 'text-gray-500 bg-white border-gray-300 hover:bg-gray-50'
                    }`;
                    button.onclick = () => goToPage(i);
                    pageNumbers.appendChild(button);
                }
            }
        }
    }

    // Navigation functions
    function changePage(direction) {
        const totalPages = Math.ceil(filteredVolunteers.length / entriesPerPage);
        if (totalPages > 0) {
            currentPage = Math.max(1, Math.min(totalPages, currentPage + direction));
            displayTable();
        }
    }

    function goToPage(page) {
        currentPage = page;
        displayTable();
    }

    // Search and filter functions
    function filterVolunteers() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const designationFilter = document.getElementById('designationFilter').value;

        filteredVolunteers = volunteers.filter(volunteer => {
            const matchesSearch = 
                volunteer.name.toLowerCase().includes(searchTerm) ||
                volunteer.reg_no.toLowerCase().includes(searchTerm) ||
                volunteer.designation.toLowerCase().includes(searchTerm);

            const matchesDesignation = !designationFilter || volunteer.designation === designationFilter;

            return matchesSearch && matchesDesignation;
        });

        currentPage = 1;
        displayTable();
    }

    // Sort table
    function sortTable(column) {
        const direction = sortColumn === column && sortDirection === 'asc' ? 'desc' : 'asc';
        sortColumn = column;
        sortDirection = direction;

        filteredVolunteers.sort((a, b) => {
            let aValue = a[column].toLowerCase();
            let bValue = b[column].toLowerCase();
            
            return direction === 'asc' ? 
                (aValue > bValue ? 1 : -1) : 
                (aValue < bValue ? 1 : -1);
        });

        displayTable();
    }

    // delete Modal functions
    function showDeleteModal(regNo) {
        document.getElementById('deleteModal').classList.remove('hidden');
        document.getElementById('confirmDeleteBtn').onclick = () => {
            window.location.href = `${DELETE_VOLUNTEER_BASE_URL}${regNo}`;
        };
    }

    function closeDeleteModal() {
        document.getElementById('deleteModal').classList.add('hidden');
    }

    // Suspend Modal function
    function showSuspendModal(regNo) {
    document.getElementById('suspendModal').classList.remove('hidden');
        document.getElementById('confirmSuspendBtn').onclick = () => {
            window.location.href = `${SUSPEND_VOLUNTEER_BASE_URL}${regNo}`;
        };
    }

    // Close suspend modal
    function closeSuspendModal() {
        document.getElementById('suspendModal').classList.add('hidden');
    }

    // Show modal for reactivation
    function showReactivateModal(regNo) {
        document.getElementById('reactivateModal').classList.remove('hidden');
        document.getElementById('confirmReactivateBtn').onclick = () => {
            window.location.href = `${REACTIVATE_VOLUNTEER_BASE_URL}${regNo}`;
        };
    }

    // Close reactivation modal
    function closeReactivateModal() {
        document.getElementById('reactivateModal').classList.add('hidden');
    }

    // Setup event listeners
    function setupEventListeners() {
        document.getElementById('searchInput').addEventListener('input', filterVolunteers);
        document.getElementById('designationFilter').addEventListener('change', filterVolunteers);
        
        document.getElementById('entriesPerPage').addEventListener('change', function() {
            entriesPerPage = parseInt(this.value);
            currentPage = 1;
            displayTable();
        });

        // Close modal when clicking outside
        document.getElementById('deleteModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeDeleteModal();
            }
        });
    }
    

    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', init);