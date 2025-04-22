<template>
    <div class="flex flex-wrap justify-center mt-10">
        <ProfileMenuCard headText="Ваши меню" bodyText="Просмотр и редактировнание данных о ваших меню" link="menu" />
        <ProfileMenuCard v-if="is_head" headText="Данные компании"
            bodyText="Просмотр и редактирование данных вашей компании" link="company-info" />
        <ProfileMenuCard v-if="is_head" headText="Добавить сотрудника" bodyText="Добавляйте сотрудников в свою компанию"
            :link="'/register/' + company_id" />

        <ProfileMenuCard headText="Ваши учетные данные"
            bodyText="Просмотр и редактирование данных вашего профиля пользователя" link="profile" />
        <ProfileMenuCard headText="Ифнормация о тарифе" bodyText="Просмотр данных о вашем тарифе" link="tarifs" />
        <ProfileMenuCard headText="Сотрудники" bodyText="Список ваших сотрудников" link="workers" />

    </div>
</template>
<script>
import ProfileMenuCard from '../components/ProfileMenuCard.vue';
import axios from 'axios';
export default {
    name: "Profile",
    components: { ProfileMenuCard },
    computed: {
        is_head() { return this.$store.state.worker.is_head },
    },
    props: {
    },
    data() {
        return {
            company_id: '0',
        }
    },
    created() {
        this.get_user()
    },
    methods: {
        async get_user() {
            await axios
                .get("/api/v1/workers/0")
                .then(response => {
                    this.company_id = response.data.company.id
                })
                .catch(error => {
                    console.log(error)
                })
        },
    },
}
</script>
