

document.addEventListener("DOMContentLoaded", function () {

    const educationForm = document.getElementById("editEducationForm");

    document.querySelectorAll(".editEducationBtn").forEach(function (btn) {

        btn.addEventListener("click", function () {

            educationForm.action = "/education/edit/" + this.dataset.id + "/";

            educationForm.querySelector("[name='education_type']").value = this.dataset.type;
            educationForm.querySelector("[name='institution_name']").value = this.dataset.institution;
            educationForm.querySelector("[name='board_or_university']").value = this.dataset.board;
            educationForm.querySelector("[name='course_name']").value = this.dataset.course;
            educationForm.querySelector("[name='specialization']").value = this.dataset.specialization;
            educationForm.querySelector("[name='percentage']").value = this.dataset.percentage;
            educationForm.querySelector("[name='cgpa']").value = this.dataset.cgpa;
            educationForm.querySelector("[name='passing_year']").value = this.dataset.year;

        });

    });

    const projectForm = document.getElementById("editProjectForm");

    document.querySelectorAll(".editProjectBtn").forEach(function (btn) {

        btn.addEventListener("click", function () {


            projectForm.action = "/project/edit/" + this.dataset.id + "/";

            projectForm.querySelector("[name='project_title']").value = this.dataset.title;
            projectForm.querySelector("[name='role']").value = this.dataset.role;
            projectForm.querySelector("[name='project_description']").value = this.dataset.description;
            projectForm.querySelector("[name='technologies_used']").value = this.dataset.technologies;
            projectForm.querySelector("[name='github_url']").value = this.dataset.github;
            projectForm.querySelector("[name='live_url']").value = this.dataset.live;
            projectForm.querySelector("[name='start_date']").value = this.dataset.start;
            projectForm.querySelector("[name='end_date']").value = this.dataset.end;

            projectForm.querySelector("[name='currently_working']").checked =
                this.dataset.currentlyworking === "true";

        });

    });




    const inputs = document.querySelectorAll(".otp-input");

    const hidden = document.getElementById("otp");

    inputs.forEach((input, index) => {

        input.addEventListener("input", function () {

            this.value = this.value.replace(/[^0-9]/g, '');

            if (this.value && index < 5) {

                inputs[index + 1].focus();

            }

            hidden.value = [...inputs].map(i => i.value).join("");

        });

        input.addEventListener("keydown", function (e) {

            if (e.key === "Backspace" && !this.value && index > 0) {

                inputs[index - 1].focus();

            }

        });

    });

    document.addEventListener("paste", function (e) {

        let paste = e.clipboardData.getData("text").trim();

        if (/^\d{6}$/.test(paste)) {

            inputs.forEach((box, i) => {

                box.value = paste[i];

            });

            hidden.value = paste;

            inputs[5].focus();

        }

    });

    let time = 60;

    let timer = document.getElementById("timer");

    let resend = document.getElementById("resendBtn");

    let countdown = setInterval(function () {

        time--;

        timer.innerHTML = time + "s";

        if (time <= 0) {

            clearInterval(countdown);

            timer.innerHTML = "OTP Expired";

            resend.classList.remove("disabled");

        }

    }, 1000);

    const inputs = document.querySelectorAll(".otp-input");
    const hidden = document.getElementById("otp");

    inputs.forEach((input, index) => {

        input.addEventListener("input", function () {

            this.value = this.value.replace(/[^0-9]/g, "");

            if (this.value && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }

            hidden.value = [...inputs].map(i => i.value).join("");
        });

        input.addEventListener("keydown", function (e) {

            if (e.key === "Backspace" && !this.value && index > 0) {
                inputs[index - 1].focus();
            }

        });

    });


});


