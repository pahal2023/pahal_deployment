// JavaScript for 4 shortcuts options.
const toggleBtn = document.getElementById('toggle-menu');
const sideMenu = document.getElementById('side-menu');
const body = document.querySelector('body');
const editShortcutsBtn = document.getElementById('editShortcutsBtn');
const editShortcutsModal = document.getElementById('editShortcutsModal');
const cancelEditBtn = document.getElementById('cancelEditBtn');
const saveShortcutsBtn = document.getElementById('saveShortcutsBtn');
const shortcutOptionsContainer = document.getElementById('shortcutOptions');
const dashboardShortcutsContainer = document.getElementById('dashboardShortcuts');
const mainNavLinksContainer = document.getElementById('mainNavLinks');
const shortcutTiles = document.querySelectorAll('.shortcut-tile');

// --- FIX: Declare currentOpenDropdown HERE at the top-level scope ---
let currentOpenDropdown = null; // Initialize it here!

// Configuration for navigation links: label -> { icon, color }
const navItemConfig = {
    'Overview': { icon: 'fa-chart-line', color: 'indigo' },
    'Time Table': { icon: 'fa-calendar-alt', color: 'green' },
    'Today Tasks': { icon: 'fa-tasks', color: 'yellow' },
    'Students Info': { icon: 'fa-info-circle', color: 'blue' },
    'Attendance': { icon: 'fa-check-square', color: 'teal' },
    'Performance': { icon: 'fa-signal', color: 'purple' },
    'Admissions': { icon: 'fa-user-plus', color: 'pink' },
    'Volunteer Info': { icon: 'fa-id-card', color: 'orange' },
    'Enrollments': { icon: 'fa-clipboard-list', color: 'lime' },
    'Attendance Analysis': { icon: 'fa-line-chart', color: 'cyan' },
    'Progress Report': { icon: 'fa-file-alt', color: 'amber' },
    'Add Tasks': { icon: 'fa-plus-circle', color: 'red' },
    'Volunteer Permissions': { icon: 'fa-key', color: 'fuchsia' },
    'General Settings': { icon: 'fa-wrench', color: 'gray' },
    'Change Password': { icon: 'fa-lock', color: 'rose' },
    'Logout': { icon: 'fa-sign-out-alt', color: 'slate' }
    // Add configurations for all your navigation items
};

// Enhanced dropdown toggle with exclusive behavior
function toggleDropdown(menuId) {
    const menu = document.getElementById(menuId);
    const arrow = document.getElementById(menuId.replace('Menu', 'Arrow'));

    // If clicking the same dropdown that's open, close it
    if (currentOpenDropdown === menuId) {
        closeDropdown(menuId);
        currentOpenDropdown = null;
        return;
    }

    // Close previously open dropdown
    if (currentOpenDropdown) {
        closeDropdown(currentOpenDropdown);
    }

    // Open the new dropdown
    openDropdown(menuId);
    currentOpenDropdown = menuId;
}

function openDropdown(menuId) {
    const menu = document.getElementById(menuId);
    const arrow = document.getElementById(menuId.replace('Menu', 'Arrow'));

    menu.classList.add('show');
    arrow.classList.add('rotated');
}

function closeDropdown(menuId) {
    const menu = document.getElementById(menuId);
    const arrow = document.getElementById(menuId.replace('Menu', 'Arrow'));

    menu.classList.remove('show');
    arrow.classList.remove('rotated');
}

// Mobile menu toggle
toggleBtn.addEventListener('click', () => {
    sideMenu.classList.toggle('-translate-x-full');
    body.classList.toggle('sidebar-open');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    // Check if the sideMenu and toggleBtn are defined before using them
    if (sideMenu && toggleBtn && window.innerWidth < 1024) {
        if (!sideMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
            sideMenu.classList.add('-translate-x-full');
            body.classList.remove('sidebar-open');
        }
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
        body.classList.remove('sidebar-open');
    }
});

// let currentShortcuts = [
//     { label: 'Students Info', href: '#' }, // Default shortcuts
//     { label: 'Add Tasks', href: '#' },
//     { label: 'Reports', href: '#' },
//     { label: 'Settings', href: '#' }
// ];

// function toggleVisibility(id) {
//     const menu = document.getElementById(id);
//     menu.classList.toggle('hidden');
// }

// editShortcutsBtn.addEventListener('click', () => {
//     editShortcutsModal.classList.remove('hidden');
//     populateShortcutOptions();
// });

// cancelEditBtn.addEventListener('click', () => {
//     editShortcutsModal.classList.add('hidden');
// });

// saveShortcutsBtn.addEventListener('click', () => {
//     const selectedOptions = Array.from(shortcutOptionsContainer.querySelectorAll('input[type="checkbox"]:checked'))
//         .map(checkbox => ({
//             label: checkbox.dataset.label,
//             href: checkbox.dataset.href
//         }))
//         .slice(0, 4);

//     updateDashboardShortcuts(selectedOptions);
//     editShortcutsModal.classList.add('hidden');
//     console.log('Saved Shortcuts:', selectedOptions);
//     // In a real application, you would also save these to the user's profile (e.g., using an AJAX request).
// });

// function populateShortcutOptions() {
//     shortcutOptionsContainer.innerHTML = '';
//     const navLinks = mainNavLinksContainer.querySelectorAll('a');

//     navLinks.forEach(link => {
//         const label = link.dataset.navLabel;
//         const href = link.getAttribute('href');
//         const config = navItemConfig[label];

//         if (label && config) {
//             const isSelected = currentShortcuts.some(shortcut => shortcut.label === label);
//             const checkbox = document.createElement('input');
//             checkbox.type = 'checkbox';
//             checkbox.value = label;
//             checkbox.dataset.label = label;
//             checkbox.dataset.href = href;
//             checkbox.dataset.icon = config.icon;
//             checkbox.dataset.color = config.color;
//             checkbox.checked = isSelected;

//             const labelElement = document.createElement('label');
//             labelElement.textContent = label;
//             labelElement.classList.add('ml-2');

//             const div = document.createElement('div');
//             div.appendChild(checkbox);
//             div.appendChild(labelElement);
//             shortcutOptionsContainer.appendChild(div);
//         }
//     });
// }

// function updateDashboardShortcuts(shortcuts) {
//     shortcuts.forEach((shortcut, index) => {
//         if (shortcutTiles[index]) {
//             const config = navItemConfig[shortcut.label];
//             const iconClass = config ? `fa fa-${config.icon} mr-2` : 'fa fa-link mr-2';
//             const bgColorClass = config ? `bg-${config.color}-100 hover:bg-${config.color}-200` : 'bg-gray-100 hover:bg-gray-200';
//             const textColorClass = config ? `text-${config.color}-700` : 'text-gray-700';

//             shortcutTiles[index].querySelector('i').className = iconClass;
//             shortcutTiles[index].querySelector('i').nextSibling.textContent = ' ' + shortcut.label;
//             shortcutTiles[index].setAttribute('href', shortcut.href);
//             shortcutTiles[index].className = `shortcut-tile ${bgColorClass} ${textColorClass} font-semibold py-4 px-2 rounded-md text-center shadow`;
//         }
//     });

//     currentShortcuts = shortcuts;

//     for (let i = shortcuts.length; i < shortcutTiles.length; i++) {
//         shortcutTiles[i].querySelector('i').className = 'fa fa-link mr-2';
//         shortcutTiles[i].querySelector('i').nextSibling.textContent = ' Empty';
//         shortcutTiles[i].setAttribute('href', '#');
//         shortcutTiles[i].className = 'shortcut-tile bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-4 px-2 rounded-md text-center shadow';
//     }
// }