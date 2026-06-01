# 🤖 Team Inovatic

<div align="center">

### World Robot Olympiad 2026  
Future Engineers

Passionate about robotics, innovation, engineering, and STEM education.

Proudly representing **Inovatic Split**

</div>

---

## 📸 Team Photo

<div align="center">
  <img src="TEAM_PHOTO_URL" width="700">
</div>

---

# 👥 Team Members

## 🧑‍💻 Josip Stepinac

<div align="center">
  <img src="https://github.com/user-attachments/assets/b899a412-e6df-4ac8-bf09-66c7db93794b" width="450">
</div>

| Information | Details |
|------------|---------|
| 🎂 Age | 22 |
| 🎓 College | PMF – Faculty of Natural Sciences and Mathematics, University of Split |

### About Me

Hi! I am **Josip Stepinac**, and robotics has been a central part of my life and personal development for many years. I have participated in numerous WRO competitions and have spent the past five years actively teaching robotics and sharing my knowledge with others.

Through robotics, I have developed strong problem-solving skills, a structured engineering mindset, and a deep understanding of how theory connects with real-world applications. It has shaped not only my technical abilities, but also the way I approach learning, teamwork, and challenges.

This is my first year competing in this WRO category, and I see it as an important opportunity to step out of my comfort zone, explore new technologies, and continue growing both technically and personally.

---

## 🧑‍💻 Ivan Stepinac

<div align="center">
  <img src="https://github.com/user-attachments/assets/6f70391f-cc8d-46d6-a2b1-11cc047bfaf2" width="420">
</div>

| Information | Details |
|------------|---------|
| 🎂 Age | 20 |
| 🎓 College | FESB – Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture, University of Split |

### About Me

Hi! I am **Ivan Stepinac**, a software developer with a strong passion for technology, innovation, and problem-solving.

A significant part of my development comes from many years of involvement in robotics and participation in WRO competitions. Robotics has played a major role in shaping my mindset, technical skills, and approach to complex challenges.

Beyond software development, I enjoy creating innovative and useful projects that can make a positive impact. One of my recent projects, **ShowMe**, is a video call application that translates sign language into text, helping improve communication for deaf and hard-of-hearing individuals.

Whether I am developing software, working on robotics, or building new applications, I am always driven by learning and creating real-world impact.

---

## 🧑‍💻 Vito Drnjević

<div align="center">
  <img src="https://github.com/user-attachments/assets/aa512ad0-b096-429c-975a-e74e61a22a05" width="420">
</div>

| Information | Details |
|------------|---------|
| 🎂 Age | 19 |
| 🎓 College | FESB – Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture, University of Split |

### About Me

Hi! I am **Vito Drnjević**, and this is my fourth season participating in the World Robot Olympiad.

After completing my final Robomission season, I decided to take on a new challenge and further expand my skills in robotics and programming. In addition to technology, I enjoy football, travelling, and exploring new experiences.

I am excited to work alongside my teammates and continue growing through engineering and innovation.

---

# 🎯 Coach

## 👨‍🏫 Jozo Pivac

<div align="center">
  <img src="COACH_PHOTO_URL" width="500">
</div>

### About Him

He is a dedicated and goal-oriented coach, university professor, and founder of the Inovatic association, with a strong focus on education, innovation, and long-term student development.

With a background in academia and hands-on experience in leading robotics and engineering teams, he combines theoretical knowledge with practical mentorship. His approach focuses on guiding students through real challenges, helping them develop technical skills, critical thinking, responsibility, and independence.

Over the years, he has played a key role in building and supporting teams within the Inovatic community, creating an environment where students can grow, experiment, and turn ideas into real engineering projects.

More than a coach, he is a mentor who connects education, research, and real-world application, shaping future engineers and innovators.

---

## 👨‍🏫 Gratitude to Our Coach

As a team, we are deeply grateful to our coach for his continuous support, guidance, and dedication throughout our entire robotics journey.

He has been with us since our earliest days in primary school, and has played a fundamental role in shaping who we are today. Over the years, he has helped us develop not only technical skills in robotics, engineering, and programming, but also discipline, teamwork, and a strong mindset for growth.

We are sincerely thankful for the opportunity he has given all three of us to experience robotics in a meaningful way and to contribute to the **Inovatic Split** community through knowledge and passion for technology.

---

# 🏆 About Inovatic

**Inovatic Split** is a STEM and robotics association dedicated to innovation, engineering, programming, and education.

Through workshops, projects, and competitions, Inovatic helps young people develop technical skills, creativity, and teamwork while preparing them for real-world challenges.

---

# 🚀 Our Mission

As Team Inovatic, we are united by a passion for robotics, engineering, and innovation.

Our mission is to develop creative solutions, continuously improve our skills, and inspire others through STEM and robotics. Through WRO, we challenge ourselves to think critically, collaborate, and turn ideas into reality.

---
# 🧠 Initial Concept – Open Challenge

At the beginning of our development process for the World Robot Olympiad Future Engineers Open Challenge, our team focused on designing a reliable and efficient method for recognizing upcoming turns on the track.

Our main goal was to improve autonomous navigation by enabling the robot to detect and react to turns in advance, ensuring smooth and stable movement throughout the run.

---

## 🎯 First Idea: Color-Based Turn Detection

Our initial concept was based on **colored guide lines placed before each turn**:

- 🟠 Orange line → Right turn  
- 🔵 Blue line → Left turn  

A dedicated **color sensor** mounted close to the track would detect these markers in real time. Once detected, the robot would immediately prepare and execute the corresponding steering action.

### Advantages of this approach:
- Fast and simple color recognition  
- Low computational complexity  
- Clear separation of left/right decision logic  
- Easy calibration during early testing  

---

## 📡 Supporting Navigation System

At the same time, our robot was equipped with **two side-mounted distance sensors**:

- Left sensor → measures distance to left wall  
- Right sensor → measures distance to right wall  

By comparing these values, the robot maintained proper centering on the track and corrected its position when drifting occurred. This ensured:
- Stable movement  
- Reduced collisions  
- Improved trajectory accuracy  

---

## ⚙️ Design Limitations & System Evaluation

As the system evolved, we carefully evaluated hardware constraints and system complexity.

We identified several limitations:

- Limited number of available sensor ports on the control hub  
- High reliance on the camera system for visual processing  
- Increased computational load when combining multiple active sensors  
- Additional weight, wiring, and mechanical complexity  

These factors could negatively impact system stability and overall performance during competition runs.

---

## 🔄 Final Decision

After discussion with our mentor, we decided to **abandon the color-based navigation system** and focus on a more streamlined approach using:

- Camera-based perception  
- Distance sensor-based centering and navigation  

This decision improved:
- System efficiency  
- Hardware simplicity  
- Overall reliability  

---

## 📚 Conclusion

Although this idea was not implemented in the final robot, it played an important role in our engineering process.

It helped us:
- Explore alternative navigation strategies  
- Understand hardware limitations  
- Improve system design thinking  
- Learn the importance of optimization in robotics  

Ultimately, this concept contributed significantly to the development of our final solution and our understanding of autonomous navigation systems.
<div align="center">
---

## 🚀 Final Idea: Distance-Based Navigation & Turn Detection

Our final approach for the Open Challenge is based on a **proportional centering system** that keeps the robot accurately aligned in the middle of the track.

This is achieved using **two side-mounted distance sensors**, where:

- The left sensor measures the distance to the left wall  
- The right sensor measures the distance to the right wall  

By continuously comparing and balancing these values, the robot maintains stable and proportional centering within the track.

In addition, **turn detection is also based on these same distance sensors**. Changes in measured distances are used to identify upcoming turns, allowing the robot to react in advance and adjust its trajectory smoothly and efficiently.

This approach provides a simplified, reliable, and tightly integrated navigation system that reduces hardware complexity while maintaining high accuracy and consistency during autonomous driving.

## ⚙️ Innovation • Creativity • Teamwork • Excellence

### Team Inovatic | WRO 2026

</div>
