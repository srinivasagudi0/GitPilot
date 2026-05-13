import streamlit as st


def Graduate():
    st.header("Congratulations!")
    st.write("You've completed the GitPilot training program!")
    st.subheader("What You've Learned:")
    st.checkbox("Initialize Git in a project")
    st.checkbox("Check status and stage files")
    st.checkbox("Commit your changes")
    st.checkbox("View logs and create branches")
    st.checkbox("Add remote and push to GitHub")
    st.checkbox("Clone repositories")
    st.write("\nYou're ready to use Git confidently!")
    st.write("Keep practicing to become a Git pro!")
    st.warning("Remember, the best way to learn Git is by using it regularly. Don't be afraid to experiment and make mistakes. Happy coding!")

    if st.button("Celebrate with Confetti!"):
        st.balloons()