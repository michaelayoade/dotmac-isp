"use strict";exports.id=2552,exports.ids=[2552],exports.modules={12705:(e,t,r)=>{r.d(t,{Jr:()=>l});var i,a,n=r(48324),s=r(47638);(function(e){e.ACTIVE="active",e.TRIALING="trialing",e.PAST_DUE="past_due",e.CANCELED="canceled",e.PAUSED="paused",e.INCOMPLETE="incomplete",e.INCOMPLETE_EXPIRED="incomplete_expired"})(i||(i={})),function(e){e.MONTHLY="monthly",e.QUARTERLY="quarterly",e.ANNUAL="annual",e.LIFETIME="lifetime"}(a||(a={}));let o=`
  query GetPlans(
    $page: Int
    $pageSize: Int
    $isActive: Boolean
    $billingCycle: BillingCycleEnum
  ) {
    plans(
      page: $page
      pageSize: $pageSize
      isActive: $isActive
      billingCycle: $billingCycle
    ) {
      plans {
        id
        name
        description
        price
        currency
        billingCycle
        trialDays
        isActive
      }
      totalCount
      hasNextPage
      hasPrevPage
      page
      pageSize
    }
  }
`;function l(e={},t=!0){let{page:r=1,pageSize:i=20,isActive:a,billingCycle:l}=e;return(0,n.a)({queryKey:["billing-plans",e],queryFn:async()=>(await s.S.request(o,{page:r,pageSize:i,isActive:a,billingCycle:l})).plans,enabled:t,staleTime:3e5})}},26576:(e,t,r)=>{r.d(t,{zG:()=>l});var i=r(29771);r(17406);let a=e=>e instanceof Error&&("status"in e||"response"in e),n=e=>{if(e instanceof Error)return e.message;if("string"==typeof e)return e;if(a(e)&&e.data){let t=e.data;if(t.message&&"string"==typeof t.message)return t.message;if(t.detail&&"string"==typeof t.detail)return t.detail}return"An unexpected error occurred. Please try again."},s=e=>a(e)?e.status:e&&"object"==typeof e&&"response"in e&&e.response&&"object"==typeof e.response&&"status"in e.response?e.response.status:void 0,o=e=>{},l=(e,t={})=>{let{showToast:r=!0,userMessage:a,redirectOnUnauthorized:l=!0,context:p,onError:c}=t,d=s(e),u=a||n(e);i.k.error("API Error",e,{status:d,message:u,...p}),(401!==d||!l)&&(403===d?r&&o({title:"Access Denied",description:"You do not have permission to perform this action.",variant:"destructive"}):404===d?r&&o({title:"Not Found",description:u,variant:"destructive"}):422===d?r&&o({title:"Validation Error",description:u,variant:"destructive"}):d&&d>=500?r&&o({title:"Server Error",description:"An unexpected server error occurred. Please try again later.",variant:"destructive"}):r&&o({title:"Error",description:u,variant:"destructive"}),c&&e instanceof Error&&c(e))}},47638:(e,t,r)=>{r.d(t,{S:()=>a});var i=r(36607);let a=function(){let e=i.LM.api.graphqlEndpoint??i.LM.api.buildUrl("/graphql");return{async request(t,r){let i=await fetch(e,{method:"POST",headers:{"Content-Type":"application/json","X-Portal-Type":"ispAdmin"},credentials:"include",body:JSON.stringify({query:t,variables:r})});if(!i.ok)throw Error(`GraphQL request failed: ${i.status} ${i.statusText}`);let a=await i.json(),[n]=a.errors??[];if(n)throw Error(n.message||"GraphQL request failed");if(!a.data)throw Error("GraphQL response missing data");return a.data}}}()},17406:(e,t,r)=>{}};