// Mock data for FixNet website

export const mockTickets = [
  {
    id: "FN-2025-001",
    device: "iPhone 15 Pro",
    issue: "Screen Cracked",
    description: "Screen cracked after dropping from table height",
    customerName: "Sarah Johnson",
    customerEmail: "sarah.j@email.com",
    customerPhone: "+1-555-0123",
    status: "In Progress",
    priority: "High",
    assignedTech: "Mike Chen",
    createdAt: "2025-01-15T10:30:00Z",
    estimatedCompletion: "2025-01-16T14:00:00Z",
    cost: 299
  },
  {
    id: "FN-2025-002",
    device: "Samsung Galaxy S24",
    issue: "Battery Issues",
    description: "Battery drains very quickly, phone gets hot during charging",
    customerName: "Alex Rodriguez",
    customerEmail: "alex.r@email.com",
    customerPhone: "+1-555-0124",
    status: "Diagnosed",
    priority: "Medium",
    assignedTech: "Lisa Wang",
    createdAt: "2025-01-15T14:20:00Z",
    estimatedCompletion: "2025-01-17T10:00:00Z",
    cost: 149
  },
  {
    id: "FN-2025-003",
    device: "Google Pixel 8",
    issue: "Water Damage",
    description: "Phone fell in water, screen flickering and speakers not working",
    customerName: "Jordan Kim",
    customerEmail: "jordan.k@email.com",
    customerPhone: "+1-555-0125",
    status: "Pending Pickup",
    priority: "High",
    assignedTech: "David Park",
    createdAt: "2025-01-16T09:15:00Z",
    estimatedCompletion: "2025-01-18T16:00:00Z",
    cost: 399
  }
];

export const deviceTypes = [
  { name: "iPhone", models: ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14", "iPhone 13", "iPhone 12", "Other iPhone"] },
  { name: "Samsung", models: ["Galaxy S24 Ultra", "Galaxy S24+", "Galaxy S24", "Galaxy S23", "Galaxy Note 20", "Galaxy A54", "Other Samsung"] },
  { name: "Google", models: ["Pixel 8 Pro", "Pixel 8", "Pixel 7", "Pixel 6", "Other Pixel"] },
  { name: "OnePlus", models: ["OnePlus 12", "OnePlus 11", "OnePlus 10", "Other OnePlus"] },
  { name: "Other", models: ["Huawei", "Xiaomi", "LG", "Motorola", "Other Brand"] }
];

export const issueTypes = [
  {
    category: "Screen Issues",
    issues: ["Cracked Screen", "Black Screen", "Screen Flickering", "Touch Not Working", "Display Lines"]
  },
  {
    category: "Battery Issues", 
    issues: ["Fast Battery Drain", "Won't Charge", "Overheating", "Battery Swelling", "Random Shutdowns"]
  },
  {
    category: "Audio Issues",
    issues: ["No Sound", "Speaker Distortion", "Microphone Not Working", "Headphone Jack Issues"]
  },
  {
    category: "Camera Issues",
    issues: ["Camera Won't Open", "Blurry Photos", "Flash Not Working", "Front Camera Issues"]
  },
  {
    category: "Network Issues",
    issues: ["No Signal", "WiFi Not Working", "Bluetooth Issues", "Mobile Data Problems"]
  },
  {
    category: "Physical Damage",
    issues: ["Water Damage", "Cracked Back", "Bent Frame", "Broken Buttons", "Charging Port Damage"]
  },
  {
    category: "Software Issues",
    issues: ["Won't Turn On", "Frozen Screen", "App Crashes", "Slow Performance", "Storage Full"]
  }
];

export const faqData = [
  {
    question: "How long does a typical repair take?",
    answer: "Most repairs are completed within 24-48 hours. Screen replacements typically take 2-4 hours, while more complex issues like water damage may take 1-3 days for proper diagnosis and repair."
  },
  {
    question: "Do you offer pickup and delivery?",
    answer: "Yes! We offer free pickup and delivery within our service areas. Simply schedule a pickup when submitting your repair request, and we'll handle the rest."
  },
  {
    question: "What's your warranty policy?",
    answer: "All repairs come with a 90-day warranty covering parts and labor. If the same issue occurs within 90 days, we'll fix it free of charge."
  },
  {
    question: "How much do repairs typically cost?",
    answer: "Costs vary by device and issue. Screen repairs typically range from $99-$399, battery replacements from $79-$149. We provide transparent pricing upfront with no hidden fees."
  },
  {
    question: "Can you repair water-damaged phones?",
    answer: "Yes, we specialize in water damage recovery. Our success rate is over 80% for devices brought in within 48 hours. We use advanced cleaning techniques and diagnostic tools."
  },
  {
    question: "Do you work on all phone brands?",
    answer: "We repair all major brands including iPhone, Samsung, Google Pixel, OnePlus, and more. If we can't fix it, we'll refer you to a specialist who can."
  }
];

export const generateTicketId = () => {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 1000);
  return `FN-${new Date().getFullYear()}-${String(timestamp).slice(-6)}${String(random).padStart(3, '0')}`;
};

export const mockChatMessages = [
  {
    id: 1,
    type: "bot",
    message: "Hi! I'm FixBot, your AI repair assistant. How can I help you today?",
    timestamp: new Date().toISOString()
  }
];

export const chatResponses = {
  "hello": "Hello! I'm here to help with your device repair needs. What seems to be the problem with your device?",
  "hi": "Hi there! I'm FixBot, your AI repair assistant. What device are you having trouble with?",
  "screen": "Screen issues are very common! Is your screen cracked, black, or having touch problems? I can help you understand repair options and costs.",
  "battery": "Battery problems can be frustrating! Is your phone dying quickly, not charging, or getting hot? Let me help you figure out the best solution.",
  "water": "Oh no! Water damage needs immediate attention. Have you turned off your device? Time is critical - the sooner we can help, the better the chances of recovery.",
  "cost": "Repair costs vary by device and issue. Screen repairs typically range from $99-$399, battery replacements from $79-$149. Would you like a specific quote for your device?",
  "time": "Most repairs take 24-48 hours. Simple fixes like screen replacements can be done in 2-4 hours, while complex issues may take 1-3 days. What type of repair do you need?",
  "default": "I understand you're having device trouble. For the best help, could you tell me: 1) What device you have, 2) What problem you're experiencing? I'm here to guide you through the repair process!"
};