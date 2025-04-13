<template>
    <div class="flex flex-wrap justify-center mt-10">
        <ProfileMenuCard headText="Ваши меню" bodyText="Просмотр и редактировнание данных о ваших меню" link="menu" />
        <ProfileMenuCard headText="Заказы" bodyText="Просмотр и редактировнание данных о заказах" link="sorders" />
        <ProfileMenuCard v-if="is_head" headText="Данные компании"
            bodyText="Просмотр и редактирование данных вашей компании" link="company-info" />
        <ProfileMenuCard v-if="is_head" headText="Добавить сотрудника" bodyText="Добавляйте сотрудников в свою компанию"
            :link="'/register/' + this.$store.state.worker.company.id" />

        <ProfileMenuCard headText="Ваши учетные данные"
            bodyText="Просмотр и редактирование данных вашего профиля пользователя" link="profile" />
        <ProfileMenuCard headText="Ифнормация о тарифе" bodyText="Просмотр данных о вашем тарифе" link="tarifs" />
        <ProfileMenuCard headText="Сотрудники" bodyText="Список ваших сотрудников" link="worker" />

    </div>
</template>
<script>
import ProfileMenuCard from '../components/ProfileMenuCard.vue';
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
        }
    },
    created() {
    },
    methods: {

    },
}
</script>
