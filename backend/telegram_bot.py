import httpx
import logging
from typing import Dict, Any
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message to the configured chat."""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10.0)
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    async def send_new_ticket_notification(self, ticket_data: Dict[str, Any]) -> bool:
        """Send notification for new repair ticket."""
        priority_emoji = {
            "Low": "🟢",
            "Medium": "🟡", 
            "High": "🟠",
            "Urgent": "🔴"
        }
        
        urgency_emoji = priority_emoji.get(ticket_data.get("priority", "Medium"), "🟡")
        
        message = f"""
🛠️ <b>New Repair Request - FixNet</b>

📱 <b>Device:</b> {ticket_data.get('deviceBrand', 'N/A')} {ticket_data.get('deviceModel', 'N/A')}
🔧 <b>Issue:</b> {ticket_data.get('specificIssue', 'N/A')}
📝 <b>Category:</b> {ticket_data.get('issueCategory', 'N/A')}

👤 <b>Customer:</b> {ticket_data.get('customerName', 'N/A')}
📞 <b>Phone:</b> {ticket_data.get('customerPhone', 'N/A')}
📧 <b>Email:</b> {ticket_data.get('customerEmail', 'N/A')}

🎫 <b>Ticket ID:</b> <code>{ticket_data.get('ticket_id', 'N/A')}</code>
{urgency_emoji} <b>Priority:</b> {ticket_data.get('priority', 'Medium')}
📍 <b>Pickup:</b> {ticket_data.get('pickupTime', 'Flexible')}

⏰ <b>Created:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}

💬 <b>Description:</b>
<i>{ticket_data.get('description', 'No description provided')[:200]}{'...' if len(ticket_data.get('description', '')) > 200 else ''}</i>
        """.strip()
        
        return await self.send_message(message)
    
    async def send_status_update_notification(self, ticket_id: str, old_status: str, new_status: str, customer_name: str) -> bool:
        """Send notification when ticket status changes."""
        status_emoji = {
            "New": "🆕",
            "In Progress": "⚙️",
            "Diagnosed": "🔍",
            "Pending Pickup": "📦",
            "Completed": "✅",
            "Cancelled": "❌"
        }
        
        old_emoji = status_emoji.get(old_status, "📋")
        new_emoji = status_emoji.get(new_status, "📋")
        
        message = f"""
📄 <b>Ticket Status Update - FixNet</b>

🎫 <b>Ticket ID:</b> <code>{ticket_id}</code>
👤 <b>Customer:</b> {customer_name}

{old_emoji} <b>From:</b> {old_status}
{new_emoji} <b>To:</b> {new_status}

⏰ <b>Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()
        
        return await self.send_message(message)
    
    async def send_contact_message_notification(self, contact_data: Dict[str, Any]) -> bool:
        """Send notification for new contact message."""
        message = f"""
📨 <b>New Contact Message - FixNet</b>

👤 <b>Name:</b> {contact_data.get('name', 'N/A')}
📧 <b>Email:</b> {contact_data.get('email', 'N/A')}
📋 <b>Subject:</b> {contact_data.get('subject', 'N/A')}

💬 <b>Message:</b>
<i>{contact_data.get('message', 'No message provided')[:300]}{'...' if len(contact_data.get('message', '')) > 300 else ''}</i>

⏰ <b>Received:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()
        
        return await self.send_message(message)

# Initialize the bot instance
TELEGRAM_BOT_TOKEN = "7983043105:AAGyFmxc3PqDfqlD7lUyPz9iGlAm2O3ANoU"
TELEGRAM_CHAT_ID = "673253772"

telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)