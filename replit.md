# Overview

Tournament Bracket Creator is a web-based application built with Streamlit that allows users to create and manage tournament brackets with voting functionality. The application supports tournament brackets with power-of-2 participant counts (4, 8, 16, 32, 64) and provides an interactive interface for bracket creation, participant management, and tournament progression tracking.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit for web interface
- **Layout**: Wide layout configuration with sidebar for bracket setup
- **State Management**: Streamlit session state for maintaining bracket data across user interactions
- **UI Components**: Form inputs for tournament setup, participant entry, and bracket visualization

## Backend Architecture
- **Core Logic**: BracketManager class handles all tournament logic and data management
- **Data Structure**: Dictionary-based bracket representation with round-based organization
- **Matchup System**: Unique ID generation for tracking individual matches across rounds
- **Seeding Algorithm**: Random shuffling of participants for fair bracket distribution

## Tournament Logic
- **Bracket Creation**: Automatic generation of tournament brackets based on participant count
- **Round Management**: Mathematical calculation of total rounds using log2 of participant count
- **Bye Handling**: Automatic advancement for participants without opponents in uneven brackets
- **Winner Tracking**: Support for match completion and winner advancement to next rounds

## Data Models
- **BracketManager**: Central class managing tournament state, participants, votes, and bracket progression
- **Matchup Structure**: Dictionary-based match representation with participants, winners, and completion status
- **Vote System**: Integrated voting mechanism for determining match outcomes

# External Dependencies

## Python Libraries
- **streamlit**: Web application framework for creating the user interface
- **pandas**: Data manipulation and analysis (imported but usage not evident in provided code)
- **random**: Participant shuffling and seeding randomization
- **math**: Mathematical operations for round calculations

## Potential Future Dependencies
- **Database System**: Currently using in-memory storage; may require database integration for persistence
- **Authentication Service**: For user management and bracket ownership
- **Real-time Updates**: WebSocket or similar technology for live bracket updates