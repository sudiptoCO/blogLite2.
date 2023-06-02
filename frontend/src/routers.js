import { createRouter, createWebHistory } from "vue-router";
import MyHome from './components/MyHome'
import CreateNew from './components/CreateNew'
import MyProfile from './components/MyProfile'
import LogIn from './components/LogIn'
import SignUp from './components/SignUp'
import MyFollowers from './components/MyFollowers'
import MyFollowings from './components/MyFollowings'
import EditPost from './components/EditPost'
import GuestView from './components/GuestView'
import UsersList from './components/UsersList'
import NavBar from './components/NavBar'
const routes = [
    {
        path: '/',
        name: 'home',
        component: MyHome
    },
    {
        path: '/create',
        name: 'create',
        component: CreateNew
    },
    {
        path: '/profile',
        name: 'profile',
        component: MyProfile
    },
    {
        path: '/login',
        name: 'login',
        component: LogIn
    },
    {
        path: '/signup',
        name: 'signup',
        component: SignUp
    },
    {
        path: '/myfollowers',
        name: 'myfollowers',
        component: MyFollowers
    },
    {
        path: '/myfollowings',
        name: 'myfollowings',
        component: MyFollowings
    },
    {
        path: '/editpost/:id',
        name: 'editpost',
        component: EditPost

    },
    {
        path: '/guestview/:id',
        name: 'guestview',
        component: GuestView

    },
    {
        path: '/userslist',
        name: 'UsersList',
        component: UsersList,
        props: (route) => ({ searchResults: route.params.searchResults }),
        parent: NavBar

    }

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
