<template>
    <div class="background" v-bind:style="backgroundStyle('./' + $route.params.id + '.jpg')">
        <table class="course-table">
            <thead class="normal-text">
            <tr>
                <td class="course-table-head widen-line table-border" :colspan="settings['weeks'].length + 1">
                    {{ settings['header'] }}
                </td>
            </tr>
            <tr>
                <td class="table-border">时间</td>
                <td v-for="(weekNum, weekIndex) in settings['weeks']" :key="weekIndex" class="table-border">
                    {{ "星期" + weekNum }}
                </td>
            </tr>
            </thead>
            <tbody class="normal-text">
            <tr v-for="(lesson, lessonIndex) in settings['lessons']" :key="lessonIndex" class="table-border">
                <td>{{ "第" + lesson + "节" }}</td>
                <td v-for="weekIndex in settings['weeks'].length" :key="weekIndex" class="course-lessons table-border">
                    <div v-for="item in courses[lessonIndex][weekIndex - 1]" :key="item">
                        {{ item }}
                    </div>
                </td>
            </tr>
            <tr>
                <td class="widen-line table-border" :colspan="settings['weeks'].length + 1">
                    {{ settings['footer'] }}
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
body {
    margin: 0;
    padding: 0;
    height: 100%;
    font-size: 0;
    line-height: 0;
}

.background {
    margin: 0;
    width: 100vw;
    height: 100vh;
    background-size: cover;
}

.widen-line {
    padding: 0.5vh 0.5vw;
}

.table-border {
    border: 1px solid black;
}

.normal-text {
    font-size: 0.8vw;
    line-height: 1.2vw;
    text-align: center;
    font-family: "YaHei Consolas Hybrid", cursive;
}

.course-table {
    top: 0;
    left: 0;
    right: 0;
    bottom: 2vh;
    width: 80vw;
    margin: auto;
    position: absolute;
    background-color: rgba(255, 255, 255, 0.55);
    box-shadow: 0 0 5vw 3.5vw rgba(255, 255, 255, 0.6);
}

.course-table-head {
    font-size: 1vw;
    line-height: 1.4vw;
}

.course-lessons {
    height: 9vh;
    width: 10.5vw;
}
</style>

<script>
import Settings from '../settings.json'

export default {
    data() {
        return {
            images: [],
            courses: [],
            imageNames: [],
            settings: Settings,
            backgroundStyles: [
                "linear-gradient(to top, #a18cd1 0%, #fbc2eb 100%)",
                "linear-gradient(to top, #fbc2eb 0%, #a6c1ee 100%)",
                "linear-gradient(to top, #fddb92 0%, #d1fdff 100%)",
                "linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%)",
                "linear-gradient(-20deg, #e9defa 0%, #fbfcdb 100%)",
                "linear-gradient(to top, #9795f0 0%, #fbc8d4 100%)",
                "linear-gradient(to top, #b3ffab 0%, #12fff7 100%)",
                "linear-gradient(-225deg, #E3FDF5 0%, #FFE6FA 100%)",
                "linear-gradient(-225deg, #2CD8D5 0%, #C5C1FF 56%, #FFBAC3 100%)",
                "linear-gradient(-225deg, #69EACB 0%, #EACCF8 48%, #6654F1 100%)"
            ],
        }
    },
    created() {
        this.imageNames = require.context("@/assets", false).keys();
        this.images = this.imageNames.map((i) => require("@/assets/" + i.split("/")[1]))
        Array(this.settings['lessons'].length).fill(0).forEach(() => {
            this.courses.push(new Array(this.settings['weeks'].length).fill(this.settings['blank']))
        })
        this.settings['courses'].forEach((i) => {
            if (0 <= i['x'] && i['x'] <= this.settings['lessons'].length
                && 0 <= i['y'] && i['y'] <= this.settings['weeks'].length) {
                this.courses[i['x']][i['y']] = i['info']
            } else {
                console.log('ignored invalid course position: (' + i['x'] + ', ' + i['y'] + ')')
            }
        })
        this.courses.forEach((l, i) => {
            const index = Array(l.length).fill(0).map((v, i) => i + 1)
                .find((j) => l[l.length - j] === this.settings['blank'])
            if (index !== -1) l[l.length - index] = this.settings['timeInfo'][i]
        })
    },
    methods: {
        backgroundStyle(name) {
            const index = this.imageNames.indexOf(name)
            return {
                backgroundImage: index === -1 ?
                    this.backgroundStyles[Math.floor(Math.random() * this.backgroundStyles.length)] :
                    'url(' + this.images[index] + ')'
            }
        }
    }
}
</script>
