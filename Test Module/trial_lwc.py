import re

# text = "Information security policy - what do international information security standards say? One of the most important information security controls, is the information security policy. This vital direction-giving document is, however, not always easy to develop and the authors thereof battle with questions such as what constitutes a policy. This results in the policy authors turning to existing sources for guidance. One of these sources is the various international information security standards. These standards are a good starting point for determining what the information security Policy should consist of, but should not be relied upon exclusively for guidance. Firstly, they are not comprehensive in their coverage and furthermore, tending to rather address the processes needed for successfully implementing the information security policy. It is far more important the information security policy must fit in with the organisation's culture and must therefore be developed with this in mind"
# text = "On-line Homework/Quiz/Exam applet: freely ()-.=+,? available Java software for evaluating performance on line The Homework/Quiz/Exam applet is a freely available Java program that can be used to evaluate student performance on line for any content authored by a teacher. It has database connectivity so that student scores are automatically recorded. It allows several different types of questions. Each question can be linked to images and detailed story problems. Three levels of feedback are provided to student responses. It allows teachers to randomize the sequence of questions and to randomize which of several options is the correct answer in multiple-choice questions. The creation and editing of questions involves menu selections, button presses, and the typing of content; no programming knowledge is required. The code is open source in order to encourage modifications that will meet individual pedagogical needs"
# print(text)
doc_string = text.lower()
doc_string = [s.strip() for s in re.split("[();\/:\.+=\-?,]", doc_string)]
doc_string = " ".join(doc_string)
# print(doc_string)


# key = "['On-line Homework/Quiz/Exam apple', 'available Java software', 'available Java program', 'student performance', 'student scores', 'available', 'Java', 'apple', 'Homework/Quiz/Exam', 'Homework/Quiz/Exam apple']"
# key = "['algorithm', 'original back-propagation algorithm', 'adaptive back-propagation algorithm', 'self-organizing algorithms IUSOCPN', 'adaptive learning rate', 'neural-fuzzy system', 'dynamic systems', 'system', 'fuzzy system', 'self-organizing']"
# print(key)
key = key.lower()
key = re.sub('[();\/:\.+=\-?,]', " ", key)
# print(key)