import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SubcatView from '../views/SubcatView.vue'
import ProductView from '../views/ProductView.vue'
import ProductList from '../views/ProductList.vue'
import AdminExp from '../views/AdminExp.vue'
import ManagerExp from '../views/ManagerExp.vue'
import UserSignup from '../views/UserSignup.vue'
import UserLogin from '../views/UserLogin.vue'
import CartView from '../views/CartView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignup
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },

  {
    path: '/subcategories/:categoryId',
    name: 'subcatview',
    component: SubcatView,
    props: true
  },
  {
    path: '/cart/:userId',
    name: 'cartview',
    component: CartView,
    props: true
  },

  {
    path: '/products/:subcategoryId',
    name: 'products',
    component: ProductList
  },
  {
    path: '/product/:productId',
    name: 'product',
    component: ProductView
  },
  {
    path: '/admin',
    name: 'admin_dashboard',
    component: AdminExp
  },
  {
    path: '/man',
    name: 'manager_dashboard',
    component: ManagerExp
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
