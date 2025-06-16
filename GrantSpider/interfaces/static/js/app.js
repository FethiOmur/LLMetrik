console.log("Web interface loading...");

// ===== GLOBAL VARIABLES =====
let isLoading = false;
let systemStatus = {
    system_ready: false,
    vector_db_ready: false,
    document_count: 0,
    chat_history_count: 0
};

// ===== DOM ELEMENTS =====
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const loadingOverlay = document.getElementById('loadingOverlay');
const statusIndicator = document.getElementById('statusIndicator');
const systemStatusEl = document.getElementById('systemStatus');
const recentQueriesEl = document.getElementById('recentQueries');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const refreshStatusBtn = document.getElementById('refreshStatusBtn');

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 AMIF Grant Assistant Web Interface başlatılıyor...');
    
    setupEventListeners();
    checkSystemStatus();
    loadChatHistory();
    
    // Başlangıç mesajını göster
    setTimeout(() => {
        updateStatusIndicator('ready', 'Sistem Hazır');
    }, 1000);
});

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // Mesaj gönderme
    sendBtn.addEventListener('click', handleSendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    
    // Örnek soruları tıklayabilir yap
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('example-item')) {
            const question = e.target.getAttribute('data-question');
            messageInput.value = question;
            messageInput.focus();
        }
    });
    
    // Kontrol butonları
    clearHistoryBtn.addEventListener('click', clearChatHistory);
    refreshStatusBtn.addEventListener('click', checkSystemStatus);
}

// ===== MESSAGE HANDLING =====
async function handleSendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isLoading) {
        return;
    }
    
    if (!systemStatus.system_ready) {
        showNotification('Sistem henüz hazır değil. Lütfen bekleyin...', 'warning');
        return;
    }
    
    // UI'yi güncelle
    addMessageToChat('user', message);
    messageInput.value = '';
    setLoading(true);
    
    // Hoşgeldin mesajını gizle
    hideWelcomeMessage();
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat('assistant', data.response, data.sources, data.timestamp);
            checkSystemStatus();
        } else {
            addMessageToChat('assistant', 'Hata: ' + data.error, [], null);
            showNotification('Sorgu işlenirken hata oluştu.', 'error');
        }
        
    } catch (error) {
        console.error('API Hatası:', error);
        addMessageToChat('assistant', 'Bağlantı hatası. Lütfen tekrar deneyin.', [], null);
        showNotification('Sunucuya bağlanılamadı.', 'error');
    } finally {
        setLoading(false);
    }
}

// ===== CHAT UI FUNCTIONS =====
function addMessageToChat(type, content, sources, timestamp) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-' + type;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = content;
    
    messageContent.appendChild(messageText);
    
    // Sources ekle (sadece assistant mesajları için)
    if (type === 'assistant' && sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'message-sources';
        
        const sourcesTitle = document.createElement('h4');
        sourcesTitle.textContent = 'Kaynaklar (' + sources.length + ')';
        sourcesDiv.appendChild(sourcesTitle);
        
        sources.forEach((source, index) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            sourceItem.textContent = (index + 1) + '. ' + source;
            sourcesDiv.appendChild(sourceItem);
        });
        
        messageContent.appendChild(sourcesDiv);
    }
    
    // Timestamp ekle
    if (timestamp) {
        const timestampDiv = document.createElement('div');
        timestampDiv.className = 'message-timestamp';
        const date = new Date(timestamp);
        timestampDiv.textContent = date.toLocaleTimeString('tr-TR');
        messageContent.appendChild(timestampDiv);
    }
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideWelcomeMessage() {
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }
}

// ===== SYSTEM STATUS =====
async function checkSystemStatus() {
    try {
        updateStatusIndicator('loading', 'Durum kontrol ediliyor...');
        
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.success) {
            systemStatus = data.status;
            updateSystemStatusUI();
            
            if (systemStatus.system_ready) {
                updateStatusIndicator('ready', 'Sistem Hazır');
            } else {
                updateStatusIndicator('error', 'Sistem Hazır Değil');
            }
        } else {
            updateStatusIndicator('error', 'Durum Alınamadı');
            showNotification('Sistem durumu kontrol edilemedi.', 'error');
        }
        
    } catch (error) {
        console.error('Status kontrol hatası:', error);
        updateStatusIndicator('error', 'Bağlantı Hatası');
        showNotification('Sunucuya bağlanılamadı.', 'error');
    }
}

function updateSystemStatusUI() {
    const statusItems = systemStatusEl.querySelectorAll('.status-item');
    
    // Sistem durumu
    updateStatusItem(statusItems[0], 
        systemStatus.system_ready ? 'Hazır' : 'Hazır Değil',
        systemStatus.system_ready ? 'ready' : 'error'
    );
    
    // Veritabanı durumu
    updateStatusItem(statusItems[1],
        systemStatus.vector_db_ready ? 'Bağlı' : 'Bağlı Değil',
        systemStatus.vector_db_ready ? 'ready' : 'error'
    );
    
    // Doküman sayısı
    updateStatusItem(statusItems[2],
        systemStatus.document_count.toLocaleString('tr-TR'),
        systemStatus.document_count > 0 ? 'ready' : 'error'
    );
    
    // Geçmiş sayısı
    updateStatusItem(statusItems[3],
        systemStatus.chat_history_count.toString(),
        'ready'
    );
}

function updateStatusItem(element, value, status) {
    const valueEl = element.querySelector('.status-value');
    valueEl.textContent = value;
    
    // Class'ları temizle ve yenisini ekle
    element.classList.remove('loading', 'ready', 'error');
    element.classList.add(status);
}

function updateStatusIndicator(status, text) {
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    statusDot.classList.remove('ready', 'error');
    statusText.textContent = text;
    
    if (status === 'ready') {
        statusDot.classList.add('ready');
    } else if (status === 'error') {
        statusDot.classList.add('error');
    }
}

// ===== CHAT HISTORY =====
async function loadChatHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.success && data.history.length > 0) {
            hideWelcomeMessage();
            
            data.history.forEach(entry => {
                addMessageToChat('user', entry.query);
                addMessageToChat('assistant', entry.response, entry.sources, entry.timestamp);
            });
        }
        
    } catch (error) {
        console.error('Geçmiş yükleme hatası:', error);
    }
}

async function clearChatHistory() {
    if (!confirm('Tüm sohbet geçmişini silmek istediğinize emin misiniz?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            location.reload();
        } else {
            showNotification('Geçmiş temizlenirken hata oluştu.', 'error');
        }
        
    } catch (error) {
        console.error('Geçmiş temizleme hatası:', error);
        showNotification('Sunucuya bağlanılamadı.', 'error');
    }
}

// ===== UTILITY FUNCTIONS =====
function setLoading(loading) {
    isLoading = loading;
    
    if (loading) {
        loadingOverlay.classList.add('active');
        sendBtn.disabled = true;
        messageInput.disabled = true;
    } else {
        loadingOverlay.classList.remove('active');
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

function showNotification(message, type) {
    console.log('[' + type.toUpperCase() + '] ' + message);
}

// Auto-refresh status
setInterval(checkSystemStatus, 30000);

console.log('✅ AMIF Grant Assistant Web Interface yüklendi!');
 