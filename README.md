# Nerd Fights ⚔️

**Settle the ultimate debates with your friends!** From ranking the best husbandos to determining the supreme pie, Nerd Fights helps you and your crew decide on the best of the best through fair competition and voting.

## 🚀 Features

### Current Features

#### 🏆 Tournament Bracket
- **Elimination-style tournaments** with head-to-head matchups
- **Real-time collaborative voting** - share the URL for friends to vote
- **Automatic tie-breaker** with coin flip functionality
- **Epic final results** with medal rankings (🥇🥈🥉)
- **Tournament statistics** showing wins, losses, and vote counts
- **Progress tracking** with visual indicators
- **"Start New Tournament" button** for easy resets

#### 🔥 Smash or Pass
- **Rate items one by one** with increment/decrement voting
- **Collaborative voting** with + and - buttons (green/red)
- **Progress tracking** through all items
- **Final rankings** with percentages and medal system
- **"Play Again" functionality** for multiple rounds

#### 🎨 User Experience
- **Easy setup** - paste lists with one item per line
- **Streamlit multipage structure** with native navigation
- **Mobile-friendly interface** with responsive design
- **Celebratory balloons** when games complete
- **Clean, intuitive UI** with emojis and clear labeling

## 📱 How to Use

### Tournament Bracket
1. Enter a tournament name
2. Select number of participants (4, 8, 16, 32, or 64)
3. Paste participant names (one per line)
4. Click "Create Bracket" 
5. Share the URL with friends to vote on matchups
6. Use "Coin Flip" for tied votes
7. Celebrate the champion! 🏆

### Smash or Pass
1. Enter items to rate (one per line)
2. Click "Start Smash or Pass"
3. Use green + buttons to add votes, red - buttons to remove votes
4. Navigate through all items
5. Click "Finish Game" to see final rankings

## 🛠 Technical Architecture

### Frontend
- **Streamlit** web framework with multipage structure
- **Responsive design** with column layouts
- **Real-time updates** with automatic rerun functionality
- **Session state management** for persistent data

### Backend Logic
- **BracketManager class** handles tournament logic and bracket generation
- **SmashOrPassManager class** manages voting and progression
- **Voting system** with increment/decrement capabilities
- **Results calculation** with percentage-based rankings

### Database
- **In-memory storage** using Streamlit session state
- **Automatic data persistence** during user sessions
- **Vote tracking** with participant-level granularity

## 🔮 Future Feature Ideas

### 🖼️ Image Integration
- [ ] **Auto-loading images** for both Tournament Bracket and Smash or Pass
  - Integrate with image search APIs (Pexels, Unsplash, etc.)
  - Automatic image fetching based on participant/item names
  
- [ ] **Image selection interface**
  - Show top 5 image results when searching
  - Allow users to choose their preferred image
  - Preview images before confirming selection
  
- [ ] **Custom image upload**
  - Fallback option when search results aren't suitable
  - Drag-and-drop or file upload interface
  - Image resizing and optimization

### 📊 Results Export
- [ ] **Markdown export** for easy sharing and documentation
  - Generate formatted results with rankings
  - Include tournament statistics and vote counts
  - Copy-paste friendly format for Discord/Reddit

- [ ] **Visual results generation**
  - Tournament bracket visualization as PNG/PDF
  - Smash or Pass results as infographic
  - Customizable themes and branding
  - Social media ready formats

### ⚡ Enhanced Voting
- [ ] **Tournament Bracket vote increment/decrement**
  - Add +/- buttons like Smash or Pass
  - Allow vote adjustments instead of single votes
  - Better for group voting sessions

- [ ] **Advanced voting options**
  - Weighted voting based on user preferences
  - Anonymous vs. named voting modes
  - Vote limits per user/session

### 🎯 Additional Features
- [ ] **Tournament templates** for common categories
- [ ] **Save/load tournaments** for repeat competitions
- [ ] **Tournament history** and statistics tracking
- [ ] **Custom scoring systems** beyond simple voting
- [ ] **Real-time notifications** when votes are cast
- [ ] **Tournament commentary** and notes feature

## 🏗️ Project Structure

```
nerd-fights/
├── Home.py                           # Main landing page
├── pages/
│   ├── 1_🏆_Tournament_Bracket.py   # Tournament functionality  
│   └── 2_🔥_Smash_or_Pass.py        # Smash or Pass functionality
├── bracket_logic.py                  # Tournament bracket management
├── smash_or_pass_logic.py           # Smash or Pass game logic
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
└── README.md                        # This file
```

## 🚀 Deployment

The app is designed to run on **Streamlit Cloud** with:
- Automatic HTTPS and custom domains
- Zero-config deployment from GitHub
- Built-in sharing and collaboration features
- Mobile-responsive interface

## 🤝 Perfect For

- **Friend group debates** about anime characters, food, movies
- **Community voting** on Discord servers or social media
- **Tournament organization** for gaming communities
- **Ranking activities** for content creators
- **Decision making** when the group can't agree
- **Fun social activities** at parties or gatherings

---

*Built with ❤️ using Streamlit. Ready to settle those debates once and for all!*