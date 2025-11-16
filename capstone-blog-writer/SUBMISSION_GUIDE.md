# Submission Guide for Google AI Agents Capstone Project

## Step 1: Create GitHub Repository
1. Go to https://github.com and create a new repository
2. Name it `automated-blog-writer-agent` or similar
3. Make it public
4. Do not initialize with README (since we have one)

## Step 2: Push Code to GitHub
```bash
cd capstone-blog-writer
git remote add origin https://github.com/yourusername/automated-blog-writer-agent.git
git branch -M main
git push -u origin main
```

## Step 3: Submit to Kaggle
1. Go to the Capstone Project competition on Kaggle
2. Submit the `writeup.md` file
3. Include the GitHub repository link in your submission
4. Ensure your submission demonstrates at least 3 key concepts:
   - ✅ Multi-agent system
   - ✅ Tools
   - ✅ Sessions & Memory
   - ✅ Observability
   - ✅ Agent evaluation

## Step 4: Optional - Create Video Demo
Record a short video demonstrating the agent in action using `uv run adk web`

## Files to Submit
- `writeup.md`: Your capstone writeup
- GitHub repository with complete code
- Optional: Demo video

## Key Concepts Demonstrated
- Multi-agent system (main agent + 4 sub-agents)
- Tools (custom + built-in Google Search)
- Sessions & Memory (ADK session management)
- Observability (logging, evaluation)
- Agent evaluation (test suite)

Good luck with your submission!