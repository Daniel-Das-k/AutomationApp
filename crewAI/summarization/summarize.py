import os
from dotenv import load_dotenv
import google.generativeai as genai

class Summarizer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

        self.prompt = """
        Generate summary of an academic paper

This pattern generates a summary of an academic paper based on the provided text. The input should be the complete text of the paper. The output is a summary including the following sections:

Title and authors of the Paper

Main Goal and Fundamental Concept

Technical Approach

Distinctive Features

Experimental Setup and Results

Advantages and Limitations

Conclusion



        """
    
    def generate_gemini_content(self, text=""):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(self.prompt + text)
            return response.text

        except Exception as e:
            raise e

    def save_to_markdown(self, filename, content):
        try:
            # Ensure the outputs directory exists
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)

            # Save the content to the specified file in the outputs folder
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w') as file:
                file.write(content)
            print(f"Summary saved to {filepath}")

        except Exception as e:
            raise e

def main():
    summarizer = Summarizer()

    # text = input("Enter YouTube Video Link: ")
    text = """
It is the science and engineering of making intelligent machines, especially intelligent computer programs. It is related to
the similar task of using computers to understand human intelligence, but AI does not have to confine itself to methods that
are biologically observable. While no consensual definition of Artificial Intelligence (AI) exists, AI is broadly characterized
as the study of computations that allow for perception, reason and action. Today, the amount of data that is generated, by
both humans and machines, far outpaces humans’ ability to absorb, interpret, and make complex decisions based on that data.
Artificial intelligence forms the basis for all computer learning and is the future of all complex decision making. This paper
examines features of artificial Intelligence, introduction, definitions of AI, history, applications, growth and achievements.
KEYWORDS- machine learning,deep learning,neural networks,Natural Language Processing and Knowledge Base System
INTRODUCTION-
Artificial Intelligence ( AI ) is the branch of computer science which deals with intelligence of machines where an intelligent agent
is a system that takes actions which maximize its chances of success. It is the study of ideas which enable computers to do the things
that make people seem intelligent. The central principles of AI include such as reasoning, knowledge, planning, learning,
communication, perception and the ability to move and manipulate objects. It is the science and engineering of making intelligent
machines, especially intelligent computer programs
ARTIFICIAL INTELLIGENCE METHODS:
Machine Learning-
It is one of the applications of AI where machines are not explicitly programmed to perform certain tasks; rather, they learn and
improve from experience automatically. Deep Learning is a subset of machine learning based on artificial neural networks for
predictive analysis. There are various machine learning algorithms, such as Unsupervised Learning, Supervised Learning, and
Reinforcement Learning. In Unsupervised Learning, the algorithm does not use classified information to act on it without any
guidance. In Supervised Learning, it deduces a function from the training data, which consists of a set of an input object and the
desired output. Reinforcement learning is used by machines to take suitable actions to increase the reward to find the best possibility
which should be taken in to account.
Natural Language Processing(NLP)
It is the interactions between computers and human language where the computers are programmed to process natural languages.
Machine Learning is a reliable technology for Natural Language Processing to obtain meaning from human languages. In NLP, the
audio of a human talk is captured by the machine. Then the audio to text conversation occurs, and then the text is processed where
the data is converted into audio. Then the machine uses the audio to respond to humans. Applications of Natural Language
Processing can be found in IVR (Interactive Voice Response) applications used in call centres, language translation applications
like Google Translate and word processors such as Microsoft Word to check the accuracy of grammar in text. However, the nature
of human languages makes the Natural Language Processing difficult because of the rules which are involved in the passing of
information using natural language, and they are not easy for the computers to understand. So NLP uses algorithms to recognize
and abstract the rules of the natural languages where the unstructured data from the human languages can be converted to a format
that is understood by the computer.
Automation & Robotics-
The purpose of Automation is to get the monotonous and repetitive tasks done by machines which also improve productivity and
in receiving cost-effective and more efficient results. Many organizations use machine learning, neural networks, and graphs in
© 2023 IJRTI | Volume 8, Issue 4 | ISSN: 2456-3315
IJRTI2304061 International Journal for Research Trends and Innovation (www.ijrti.org) 357
automation. Such automation can prevent fraud issues while financial transactions online by using CAPTCHA technology. Robotic
process automation is programmed to perform high volume repetitive tasks which can adapt to the change in different circumstances.
Machine Vision-
Machines can capture visual information and then analyze it. Here cameras are used to capture the visual information, the analogue
to digital conversion is used to convert the image to digital data, and digital signal processing is employed to process the data. Then
the resulting data is fed to a computer. In machine vision, two vital aspects are sensitivity, which is the ability of the machine to
perceive impulses that are weak and resolution, the range to which the machine can distinguish the objects. The usage of machine
vision can be found in signature identification, pattern recognition, and medical image analysis, etc.
Knowledge-Based Systems(KBS):
A KBS can be defined as a computer system capable of giving advice in a particular domain, utilizing knowledge provided by a
human expert. A distinguishing feature of KBS lies in the separation behind the knowledge, which can be represented in a number
of ways such as rules, frames, or cases, and the inference engine or algorithm which uses the knowledge base to arrive at a
conclusion.
Neural Networks:
NNs are biologically inspired systems consisting of a massively connected network of computational “neurons,” organized in layers.
By adjusting the weights of the network, NNs can be “trained” to approximate virtually any nonlinear function to a required degree
of accuracy. NNs typically are provided with a set of input and output exemplars. A learning algorithm (such as back propagation)
would then be used to adjust the weights in the network so that the network would give the desired output, in a type of learning
commonly called supervised learning.
Applications of AI
Artificial Intelligence has various applications in today's society. It is becoming essential for today's time because it can solve
complex problems with an efficient way in multiple industries, such as Healthcare, entertainment, finance, education, etc. AI is
making our daily life more comfortable and fast.
Following are some sectors which have the application of Artificial Intelligence:
© 2023 IJRTI | Volume 8, Issue 4 | ISSN: 2456-3315
IJRTI2304061 International Journal for Research Trends and Innovation (www.ijrti.org) 358
1. AI in Astronomy
o Artificial Intelligence can be very useful to solve complex universe problems. AI technology can be helpful for
understanding the universe such as how it works, origin, etc.
2. AI in Healthcare
o In the last, five to ten years, AI becoming more advantageous for the healthcare industry and going to have a significant
impact on this industry.
o Healthcare Industries are applying AI to make a better and faster diagnosis than humans. AI can help doctors with
diagnoses and can inform when patients are worsening so that medical help can reach to the patient before hospitalization.
3. AI in Gaming
o AI can be used for gaming purpose. The AI machines can play strategic games like chess, where the machine needs to
think of a large number of possible places.
4. AI in Finance
o AI and finance industries are the best matches for each other. The finance industry is implementing automation, chatbot,
adaptive intelligence, algorithm trading, and machine learning into financial processes.
5. AI in Data Security
o The security of data is crucial for every company and cyber-attacks are growing very rapidly in the digital world. AI can
be used to make your data more safe and secure. Some examples such as AEG bot, AI2 Platform,are used to determine
software bug and cyber-attacks in a better way.
6. AI in Social Media
o Social Media sites such as Facebook, Twitter, and Snapchat contain billions of user profiles, which need to be stored and
managed in a very efficient way. AI can organize and manage massive amounts of data. AI can analyze lots of data to
identify the latest trends, hashtag, and requirement of different users.
7. AI in Travel & Transport
o AI is becoming highly demanding for travel industries. AI is capable of doing various travel related works such as from
making travel arrangement to suggesting the hotels, flights, and best routes to the customers. Travel industries are using
AI-powered chatbots which can make human-like interaction with customers for better and fast response.
8. AI in Automotive Industry
o Some Automotive industries are using AI to provide virtual assistant to their user for better performance. Such as Tesla
has introduced TeslaBot, an intelligent virtual assistant.
o Various Industries are currently working for developing self-driven cars which can make your journey more safe and
secure.
9. AI in Robotics:
o Artificial Intelligence has a remarkable role in Robotics. Usually, general robots are programmed such that they can
perform some repetitive task, but with the help of AI, we can create intelligent robots which can perform tasks with their
own experiences without pre-programmed.
o Humanoid Robots are best examples for AI in robotics, recently the intelligent Humanoid robot named as Erica and Sophia
has been developed

"""
    if text:
        content = summarizer.generate_gemini_content(text)
        summarizer.save_to_markdown("summary.md", content)

# if __name__ == "__main__":
#     main()
