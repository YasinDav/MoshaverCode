// From index.html

// Initialize AOS
AOS.init({
    duration: 800,
    easing: 'ease-out',
    once: true
});

// Initialize Lucide icons
lucide.createIcons();

// Set current year
document.getElementById('currentYear').textContent = new Date().getFullYear();

// Support Widget Functionality
let supportWidgetOpen = false;

function toggleSupportWidget() {
    const popup = document.getElementById('supportPopup');
    supportWidgetOpen = !supportWidgetOpen;

    if (supportWidgetOpen) {
        popup.classList.add('show');
    } else {
        popup.classList.remove('show');
    }
}

function closeSupportWidget() {
    const popup = document.getElementById('supportPopup');
    popup.classList.remove('show');
    supportWidgetOpen = false;
}

// Close support popup when clicking the close button
document.getElementById('closeSupportPopup').addEventListener('click', closeSupportWidget);

// Close support popup when clicking outside
document.addEventListener('click', function (event) {
    const popup = document.getElementById('supportPopup');
    const btn = document.getElementById('supportBtn');

    if (supportWidgetOpen && !popup.contains(event.target) && !btn.contains(event.target)) {
        closeSupportWidget();
    }
});

// Quick help functionality
function showQuickHelp(topic) {
    let message = '';
    switch (topic) {
        case 'major':
            message = 'برای انتخاب رشته، ابتدا علایق و استعدادهای خود را شناسایی کنید. سپس بازار کار و آینده شغلی رشته‌های مختلف را بررسی کنید.';
            break;
        case 'study':
            message = 'برای برنامه‌ریزی مؤثر مطالعه، اهداف کوتاه‌مدت و بلندمدت تعیین کنید، زمان‌بندی منظم داشته باشید و از تکنیک‌های مطالعه فعال استفاده کنید.';
            break;
        case 'career':
            message = 'برای راهنمایی شغلی، مهارت‌های خود را توسعه دهید، تجربه عملی کسب کنید و با متخصصان حوزه مورد نظرتان ارتباط برقرار کنید.';
            break;
    }
    alert(message);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.backgroundColor = 'white';
        navbar.style.backdropFilter = 'none';
    }
});

// Add typing animation to chat messages
function addTypingAnimation() {
    const messages = document.querySelectorAll('.chat-message');
    messages.forEach((message, index) => {
        message.style.animationDelay = `${index * 0.5}s`;
    });
}

// Initialize typing animation when page loads
document.addEventListener('DOMContentLoaded', addTypingAnimation);

// Add hover effects to team cards
document.querySelectorAll('.team-card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-8px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add click animation to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function (e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        this.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
            .btn {
                position: relative;
                overflow: hidden;
            }
            
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple-animation 0.6s linear;
                pointer-events: none;
            }
            
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
document.head.appendChild(style);

// From login.html


// Initialize AOS
AOS.init();

// Initialize Lucide icons
lucide.createIcons();

// Form elements
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const passwordToggle = document.getElementById('passwordToggle');
const passwordIcon = document.getElementById('passwordIcon');
const loginBtn = document.getElementById('loginBtn');
const loginBtnText = document.getElementById('loginBtnText');
const loginSpinner = document.getElementById('loginSpinner');

// Error elements
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');

// Password toggle functionality
passwordToggle.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Update icon
    passwordIcon.setAttribute('data-lucide', type === 'password' ? 'eye' : 'eye-off');
    lucide.createIcons();
});

// Form validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateForm() {
    let isValid = true;

    // Clear previous errors
    emailError.textContent = '';
    passwordError.textContent = '';
    emailInput.classList.remove('is-invalid');
    passwordInput.classList.remove('is-invalid');

    // Validate email
    if (!emailInput.value.trim()) {
        emailError.textContent = 'Email is required';
        emailInput.classList.add('is-invalid');
        isValid = false;
    } else if (!validateEmail(emailInput.value)) {
        emailError.textContent = 'Please enter a valid email address';
        emailInput.classList.add('is-invalid');
        isValid = false;
    }

    // Validate password
    if (!passwordInput.value.trim()) {
        passwordError.textContent = 'Password is required';
        passwordInput.classList.add('is-invalid');
        isValid = false;
    } else if (passwordInput.value.length < 6) {
        passwordError.textContent = 'Password must be at least 6 characters';
        passwordInput.classList.add('is-invalid');
        isValid = false;
    }

    return isValid;
}

// Clear errors on input
emailInput.addEventListener('input', function () {
    if (emailError.textContent) {
        emailError.textContent = '';
        emailInput.classList.remove('is-invalid');
    }
});

passwordInput.addEventListener('input', function () {
    if (passwordError.textContent) {
        passwordError.textContent = '';
        passwordInput.classList.remove('is-invalid');
    }
});

// Form submission
loginForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (!validateForm()) {
        return;
    }

    // Show loading state
    loginBtn.disabled = true;
    loginBtnText.textContent = 'Signing in...';
    loginSpinner.classList.remove('d-none');

    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Simulate success/error randomly
        const isSuccess = Math.random() > 0.3;

        if (isSuccess) {
            await Swal.fire({
                icon: 'success',
                title: 'Login Successful!',
                text: 'Welcome back to v0 Counselor. Redirecting to your dashboard...',
                timer: 3000,
                timerProgressBar: true,
                showConfirmButton: false,
                position: 'top'
            });

            // Redirect to dashboard (placeholder)
            setTimeout(() => {
                window.location.href = '#dashboard';
            }, 1500);
        } else {
            await Swal.fire({
                icon: 'error',
                title: 'Login Failed',
                text: 'Invalid email or password. Please check your credentials and try again.',
                confirmButtonColor: '#0284c7'
            });
        }
    } catch (error) {
        await Swal.fire({
            icon: 'error',
            title: 'Connection Error',
            text: 'Unable to connect to the server. Please check your internet connection and try again.',
            confirmButtonColor: '#0284c7'
        });
    } finally {
        // Reset loading state
        loginBtn.disabled = false;
        loginBtnText.textContent = 'Sign In';
        loginSpinner.classList.add('d-none');
    }
});

// From messages.html

// Initialize AOS
AOS.init({
    duration: 800,
    easing: 'ease-out',
    once: true
});

// Initialize Lucide icons
lucide.createIcons();

// Mock conversations data
const conversations = [
    {
        id: "1",
        name: "مشاور هوش مصنوعی",
        avatar: "/placeholder.svg?height=48&width=48",
        lastMessage: "چطور می‌تونم در انتخاب رشته کمکتون کنم؟",
        time: "۱۰ دقیقه پیش",
        unread: true,
        online: true,
        type: "ai"
    },
    {
        id: "2",
        name: "دکتر احمد رضایی",
        avatar: "/placeholder.svg?height=48&width=48",
        lastMessage: "جلسه مشاوره فردا ساعت ۱۰ صبح",
        time: "۲ ساعت پیش",
        unread: false,
        online: false,
        type: "human"
    },
    {
        id: "3",
        name: "گروه مطالعه علوم کامپیوتر",
        avatar: "/placeholder.svg?height=48&width=48",
        lastMessage: "کسی تکلیف ریاضی رو حل کرده؟",
        time: "۵ ساعت پیش",
        unread: true,
        online: true,
        type: "group"
    },
    {
        id: "4",
        name: "مریم احمدی",
        avatar: "/placeholder.svg?height=48&width=48",
        lastMessage: "ممنون از راهنمایی‌هات!",
        time: "دیروز",
        unread: false,
        online: true,
        type: "human"
    }
];

// Mock messages data
const messagesData = {
    "1": [
        {
            id: "1",
            sender: "ai",
            text: "سلام سارا! امیدوارم روز خوبی داشته باشی. چطور می‌تونم امروز در مسیر تحصیلی‌ت کمکت کنم؟",
            time: "۱۰:۳۰",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "2",
            sender: "user",
            text: "سلام! من در مورد انتخاب بین رشته علوم کامپیوتر و طراحی گرافیک سردرگم هستم. می‌تونی کمکم کنی؟",
            time: "۱۰:۳۲",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "3",
            sender: "ai",
            text: "البته! این انتخاب مهمی هست. بذار چند سوال ازت بپرسم تا بهتر بتونم راهنمایی‌ت کنم:\n\n۱. بیشتر به حل مسائل منطقی علاقه داری یا به خلاقیت بصری؟\n۲. آینده شغلی کدوم حوزه بیشتر جذابت می‌کنه؟\n۳. با برنامه‌نویسی آشنایی داری؟",
            time: "۱۰:۳۳",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "4",
            sender: "user",
            text: "خب، من هم به حل مسائل منطقی علاقه دارم و هم به طراحی. برنامه‌نویسی هم یکم بلدم، پایتون و جاوااسکریپت.",
            time: "۱۰:۳۵",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "5",
            sender: "ai",
            text: "عالی! با توجه به علایقت، چند گزینه پیشنهاد می‌دم:\n\n🎯 **رشته‌های ترکیبی:**\n• طراحی تعامل (Interaction Design)\n• مهندسی نرم‌افزار با تمرکز روی UI/UX\n• علوم کامپیوتر با گرایش گرافیک\n\n💡 **نکته:** می‌تونی علوم کامپیوتر بخونی و در کنارش دوره‌های طراحی بگذرونی.",
            time: "۱۰:۳۷",
            avatar: "/placeholder.svg?height=40&width=40"
        }
    ],
    "2": [
        {
            id: "1",
            sender: "human",
            text: "سلام سارا، امیدوارم حالت خوب باشه.",
            time: "۰۸:۱۵",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "2",
            sender: "user",
            text: "سلام دکتر رضایی، ممنونم حالم خوبه.",
            time: "۰۸:۲۰",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "3",
            sender: "human",
            text: "جلسه مشاوره فردا ساعت ۱۰ صبح تو دفتر من. لطفاً مدارک تحصیلی‌ت رو همراه بیار.",
            time: "۰۸:۲۱",
            avatar: "/placeholder.svg?height=40&width=40"
        },
        {
            id: "4",
            sender: "user",
            text: "چشم، حتماً. ممنونم از وقتی که می‌ذارید.",
            time: "۰۸:۲۵",
            avatar: "/placeholder.svg?height=40&width=40"
        }
    ]
};

let currentConversation = null;
let currentFilter = 'all';
let isTyping = false;

// Load conversations list
function loadConversations(searchTerm = '') {
    const container = document.getElementById('conversationsList');
    let filteredConversations = conversations;

    // Apply search filter
    if (searchTerm) {
        filteredConversations = conversations.filter(conv =>
            conv.name.includes(searchTerm) || conv.lastMessage.includes(searchTerm)
        );
    }

    // Apply type filter
    if (currentFilter !== 'all') {
        if (currentFilter === 'unread') {
            filteredConversations = filteredConversations.filter(conv => conv.unread);
        } else if (currentFilter === 'ai') {
            filteredConversations = filteredConversations.filter(conv => conv.type === 'ai');
        }
    }

    if (filteredConversations.length === 0) {
        container.innerHTML = `
                    <div class="empty-state p-4">
                        <i data-lucide="message-circle" class="empty-state-icon"></i>
                        <p>هیچ گفتگویی یافت نشد</p>
                    </div>
                `;
    } else {
        container.innerHTML = filteredConversations.map(conv => `
                    <div class="conversation-list-item ${currentConversation === conv.id ? 'active' : ''}" 
                         onclick="selectConversation('${conv.id}')" data-aos="fade-up">
                        <div class="d-flex align-items-center gap-3">
                            <div class="position-relative">
                                <img src="${conv.avatar}" alt="${conv.name}" class="conversation-avatar">
                                <div class="online-status ${conv.online ? '' : 'offline-status'}"></div>
                            </div>
                            <div class="flex-grow-1">
                                <div class="conversation-name">${conv.name}</div>
                                <div class="conversation-preview">${conv.lastMessage}</div>
                                <div class="conversation-time">${conv.time}</div>
                            </div>
                            ${conv.unread ? '<div class="unread-badge"></div>' : ''}
                        </div>
                    </div>
                `).join('');
    }

    lucide.createIcons();
    AOS.refresh();
}

// Load chat messages
function loadChat(conversationId) {
    const chatArea = document.getElementById('chatArea');
    const conversation = conversations.find(c => c.id === conversationId);
    const messages = messagesData[conversationId] || [];

    if (!conversation) {
        chatArea.innerHTML = `
                    <div class="empty-state">
                        <i data-lucide="message-circle" class="empty-state-icon"></i>
                        <h3>گفتگویی انتخاب نشده</h3>
                        <p>برای شروع، یکی از گفتگوها را انتخاب کنید</p>
                    </div>
                `;
        return;
    }

    chatArea.innerHTML = `
                <!-- Chat Header -->
                <div class="messages-header">
                    <div class="d-flex align-items-center justify-content-between">
                        <div class="d-flex align-items-center gap-3">
                            <button class="btn btn-light d-md-none" id="backToSidebar">
                                <i data-lucide="arrow-right" width="20" height="20"></i>
                            </button>
                            <div class="position-relative">
                                <img src="${conversation.avatar}" alt="${conversation.name}" class="conversation-avatar">
                                <div class="online-status ${conversation.online ? '' : 'offline-status'}"></div>
                            </div>
                            <div>
                                <h3 class="h6 mb-0">${conversation.name}</h3>
                                <small class="text-light opacity-75">
                                    ${conversation.online ? 'آنلاین' : 'آفلاین'}
                                </small>
                            </div>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-light btn-sm">
                                <i data-lucide="phone" width="16" height="16"></i>
                            </button>
                            <button class="btn btn-light btn-sm">
                                <i data-lucide="video" width="16" height="16"></i>
                            </button>
                            <button class="btn btn-light btn-sm">
                                <i data-lucide="more-vertical" width="16" height="16"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Messages List -->
                <div class="messages-list" id="messagesList">
                    ${messages.map(message => `
                        <div class="message ${message.sender === 'user' ? 'sent' : ''} fade-in-up">
                            <img src="${message.avatar}" alt="Avatar" class="message-avatar">
                            <div class="message-content">
                                <div class="message-text">${message.text.replace(/\n/g, '<br>')}</div>
                                <div class="message-time">${message.time}</div>
                            </div>
                        </div>
                    `).join('')}
                    <div id="typingIndicator"></div>
                </div>

                <!-- Message Input -->
                <div class="message-input-area">
                    <div class="d-flex align-items-end gap-3">
                        <button class="btn btn-outline-primary btn-sm">
                            <i data-lucide="paperclip" width="16" height="16"></i>
                        </button>
                        <div class="flex-grow-1">
                            <textarea class="form-control message-input" placeholder="پیام خود را بنویسید..." 
                                     id="messageInput" rows="1"></textarea>
                        </div>
                        <button class="send-button" id="sendButton" disabled>
                            <i data-lucide="send" width="16" height="16"></i>
                        </button>
                    </div>
                </div>
            `;

    lucide.createIcons();
    setupMessageInput();
    scrollToBottom();

    // Setup back button for mobile
    const backButton = document.getElementById('backToSidebar');
    if (backButton) {
        backButton.addEventListener('click', () => {
            document.getElementById('messagesSidebar').classList.remove('show');
        });
    }
}

// Setup message input functionality
function setupMessageInput() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    if (!messageInput || !sendButton) return;

    messageInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 96) + 'px';

        sendButton.disabled = !this.value.trim();
    });

    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);
}

// Send message
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const messageText = messageInput.value.trim();

    if (!messageText || !currentConversation) return;

    const messagesList = document.getElementById('messagesList');
    const typingIndicator = document.getElementById('typingIndicator');

    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'message sent fade-in-up';
    userMessage.innerHTML = `
                <img src="/placeholder.svg?height=40&width=40" alt="شما" class="message-avatar">
                <div class="message-content">
                    <div class="message-text">${messageText.replace(/\n/g, '<br>')}</div>
                    <div class="message-time">${getCurrentTime()}</div>
                </div>
            `;

    messagesList.insertBefore(userMessage, typingIndicator);
    messageInput.value = '';
    messageInput.style.height = 'auto';
    document.getElementById('sendButton').disabled = true;

    scrollToBottom();

    // Show typing indicator for AI response
    if (conversations.find(c => c.id === currentConversation)?.type === 'ai') {
        showTypingIndicator();

        // Simulate AI response after delay
        setTimeout(() => {
            hideTypingIndicator();
            addAIResponse(messageText);
        }, 2000 + Math.random() * 2000);
    }

    // Update conversation preview
    updateConversationPreview(currentConversation, messageText);
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.innerHTML = `
                    <div class="typing-indicator">
                        <img src="/placeholder.svg?height=40&width=40" alt="AI" class="message-avatar">
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                        <span class="small text-muted me-2">در حال تایپ...</span>
                    </div>
                `;
        scrollToBottom();
    }
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.innerHTML = '';
    }
}

// Add AI response
function addAIResponse(userMessage) {
    const messagesList = document.getElementById('messagesList');
    const typingIndicator = document.getElementById('typingIndicator');

    // Generate AI response based on user message
    let aiResponse = generateAIResponse(userMessage);

    const aiMessage = document.createElement('div');
    aiMessage.className = 'message fade-in-up';
    aiMessage.innerHTML = `
                <img src="/placeholder.svg?height=40&width=40" alt="AI" class="message-avatar">
                <div class="message-content">
                    <div class="message-text">${aiResponse.replace(/\n/g, '<br>')}</div>
                    <div class="message-time">${getCurrentTime()}</div>
                </div>
            `;

    messagesList.insertBefore(aiMessage, typingIndicator);
    scrollToBottom();

    // Update conversation preview
    updateConversationPreview(currentConversation, aiResponse);
}

// Generate AI response
function generateAIResponse(userMessage) {
    const responses = [
        "این سوال جالبی هست! بذار بیشتر بررسی کنیم...",
        "بر اساس اطلاعاتی که دادی، پیشنهاد می‌کنم...",
        "خیلی خوب! این نکته مهمی هست که اشاره کردی.",
        "می‌تونم چند راهکار عملی بهت پیشنهاد بدم:",
        "این موضوع رو از زوایه مختلف بررسی کنیم...",
    ];

    return responses[Math.floor(Math.random() * responses.length)];
}

// Update conversation preview
function updateConversationPreview(conversationId, message) {
    const conversation = conversations.find(c => c.id === conversationId);
    if (conversation) {
        conversation.lastMessage = message.length > 50 ? message.substring(0, 50) + '...' : message;
        conversation.time = 'الان';
        loadConversations();
    }
}

// Get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('fa-IR', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

// Scroll to bottom
function scrollToBottom() {
    const messagesList = document.getElementById('messagesList');
    if (messagesList) {
        setTimeout(() => {
            messagesList.scrollTop = messagesList.scrollHeight;
        }, 100);
    }
}

// Select conversation
function selectConversation(conversationId) {
    currentConversation = conversationId;

    // Mark as read
    const conversation = conversations.find(c => c.id === conversationId);
    if (conversation) {
        conversation.unread = false;
    }

    loadConversations();
    loadChat(conversationId);

    // Hide sidebar on mobile
    if (window.innerWidth < 768) {
        document.getElementById('messagesSidebar').classList.remove('show');
    }
}

// Search functionality
document.getElementById('searchInput').addEventListener('input', function (e) {
    loadConversations(e.target.value);
});

// Filter functionality
document.querySelectorAll('[data-filter]').forEach(button => {
    button.addEventListener('click', function () {
        // Remove active class from all buttons
        document.querySelectorAll('[data-filter]').forEach(btn => {
            btn.classList.remove('active');
        });

        // Add active class to clicked button
        this.classList.add('active');

        // Update filter
        currentFilter = this.getAttribute('data-filter');
        loadConversations();
    });
});

// Sidebar toggle for mobile
document.getElementById('sidebarToggle').addEventListener('click', function () {
    document.getElementById('messagesSidebar').classList.toggle('show');
});

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    loadConversations();

    // Load first conversation by default
    if (conversations.length > 0) {
        selectConversation(conversations[0].id);
    } else {
        document.getElementById('chatArea').innerHTML = `
                    <div class="empty-state">
                        <i data-lucide="message-circle" class="empty-state-icon"></i>
                        <h3>هیچ پیامی وجود ندارد</h3>
                        <p>هنوز هیچ گفتگویی شروع نکرده‌اید</p>
                        <button class="btn btn-primary mt-3">
                            <i data-lucide="plus" width="16" height="16" class="me-2"></i>
                            شروع گفتگوی جدید
                        </button>
                    </div>
                `;
    }
});

// Handle window resize
window.addEventListener('resize', function () {
    if (window.innerWidth >= 768) {
        document.getElementById('messagesSidebar').classList.remove('show');
    }
});
    