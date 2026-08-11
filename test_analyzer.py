from resume_analyzer import analyze_resume

sample_text = """
Niti Mishra
B.Tech Computer Science, AKTU

Skills: Python, Machine Learning, Deep Learning
Tools: Git, Docker, VS Code
Projects: Face Recognition Attendance System using OpenCV
"""

result = analyze_resume(sample_text)
print(result)